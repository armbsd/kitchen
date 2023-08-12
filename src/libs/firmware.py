import os

def firmware_port_test(port_name, firmware_binary):
    firmware_path = f"/usr/local/share/{port_name}"
    firmware_file_path = os.path.join(firmware_path, firmware_binary)

    if not os.path.exists(firmware_file_path):
        print(f"Please install sysutils/{port_name} and re-run this script.")
        print(f"You can do this with:")
        print(f"  $ sudo pkg install sysutils/{port_name}")
        print("or by building the port:")
        print(f"  $ cd /usr/ports/sysutils/{port_name}")
        print("  $ make -DBATCH all install")
        exit(1)

    print("Found firmware port in:")
    print(f"    {firmware_path}")

# Example usage
# firmware_port_test("example_port", "firmware.bin")