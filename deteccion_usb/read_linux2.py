import subprocess
import re

def get_usb_drive_labels():
    result = subprocess.run(['blkid'], capture_output=True, text=True)
    output_lines = result.stdout.strip().split('\n')

    usb_drive_labels = {}
    device_path = label = None

    for line in output_lines:
        if match := re.match(r'^(.+?):\s+.*LABEL="([^"]+)"', line):
            device_path, label = match.groups()
            usb_drive_labels[device_path] = label

    return usb_drive_labels

if __name__ == "__main__":
    usb_drive_labels = get_usb_drive_labels()

    if usb_drive_labels:
        print("Nombres de dispositivos USB:")
        for device_path, label in usb_drive_labels.items():
            print(f"Dispositivo: {device_path}, Nombre: {label}")
    else:
        print("No se encontraron nombres de dispositivos USB.")
