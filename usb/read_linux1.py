import pyudev

def detect_usb_devices_linux():
    context = pyudev.Context()
    usb_devices = []

    for device in context.list_devices(subsystem='usb'):
        usb_device_info = {}
        
        for key, value in device.items():
            usb_device_info[key] = value

        usb_devices.append(usb_device_info)

    return usb_devices

if __name__ == "__main__":
    usb_devices = detect_usb_devices_linux()

    if usb_devices:
        print("Parámetros de dispositivos USB detectados en Linux:")
        for idx, device_info in enumerate(usb_devices, start=1):
            print(f"Dispositivo {idx}:")
            for key, value in device_info.items():
                print(f"  {key}: {value}")
            print("=" * 40)
    else:
        print("No se encontraron dispositivos USB en Linux.")
