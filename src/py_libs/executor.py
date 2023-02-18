import fcntl
import os
import subprocess
import threading
from time import sleep
import logging

import asyncio

log = logging.getLogger(__name__)

class ExecutionPipe:
    def __init__(self, cmd):
        self.check_period = 0.01
        self.cmd = cmd
        self.stdout = ""
        self.stderr = ""
        self.retcode = None
        self.thread = None

        self.stdout_printer = None
        self.stderr_printer = None

        self.pipe = subprocess.Popen(cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True if type(cmd) is not list else False)
        fl = fcntl.fcntl(self.pipe.stdout, fcntl.F_GETFL)  # get flags for file desriptor
        fle = fcntl.fcntl(self.pipe.stderr, fcntl.F_GETFL)  # get flags for file desriptor
        fcntl.fcntl(self.pipe.stdout, fcntl.F_SETFL, fl | os.O_NONBLOCK)  # set nonblocking on read
        fcntl.fcntl(self.pipe.stderr, fcntl.F_SETFL, fle | os.O_NONBLOCK)  # set nonblocking on read

    def run(self):
        self.thread = threading.Thread(target=self._perform)
        self.thread.start()

    def poll(self):
        if not self.thread.is_alive():
            self.retcode = self.pipe.returncode
        return self.retcode, self.stdout, self.stderr

    def wait(self, timeout=0):
        if timeout:
            self.thread.join(timeout)
            if self.thread.is_alive():
                self.pipe.terminate()
                self.thread.join(0.3)
                # It's possible that process will continue to run after receiving SIGTEM
                if self.thread.is_alive():
                    self.pipe.kill()
                    self.thread.join(0.3)
        else:
            self.thread.join()
        self.pipe.stdout.close()
        self.pipe.stderr.close()
        self.retcode = self.pipe.returncode
        return self.retcode, self.stdout, self.stderr

    def set_stdout_printer(self, printer):
        self.stdout_printer = printer

    def set_stderr_printer(self, printer):
        self.stderr_printer = printer

    def is_running(self):
        return self.thread.is_alive()

    def stop(self):
        self.pipe.terminate()
        self.thread.join(0.01)

    def _read_std(self):
        try:
            data = self.pipe.stdout.read()
            self._update_stdout(data)
            self._call_stdout_printer(data)
        except Exception as err:
            log.warning(f"{err}\nRetry...")
        try:
            data = self.pipe.stderr.read()
            self._update_stderr(data)
            self._call_stderr_printer(data)
        except Exception as err:
            log.warning(f"{err}\nFail!")

    def _perform(self):
        loop = asyncio.new_event_loop() 
        asyncio.set_event_loop(loop)
        while self.pipe.poll() is None:
            self._read_std()
            sleep(self.check_period)
        self._read_std()
        loop.close()

    def _update_stdout(self, msg):
        if msg:
            self.stdout += msg.decode("utf-8")

    def _update_stderr(self, msg):
        if msg:
            self.stderr += msg.decode("utf-8")

    def _call_stdout_printer(self, data):
        if self.stdout_printer and data:
            self.stdout_printer(data.decode("utf-8"))

    def _call_stderr_printer(self, data):
        if self.stderr_printer and data:
            self.stderr_printer(data.decode("utf-8"))


def execute(cmd, timeout=0, printstdout=None, printstderr=None):
    pipe = ExecutionPipe(cmd)
    if printstdout:
        pipe.set_stdout_printer(printstdout)
    if printstderr:
        pipe.set_stderr_printer(printstderr)
    pipe.run()
    return pipe.wait(timeout)