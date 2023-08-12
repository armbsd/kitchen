def email_status(subject, message):
    if EMAIL:
        subprocess.run(["echo", message, "|", "mail", "-s", subject, EMAIL], shell=True)

# Example usage
# subject = "Notification Subject"
# message = "This is a notification message."
# email_status(subject, message)