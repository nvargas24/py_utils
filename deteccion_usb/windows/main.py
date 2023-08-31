import win32com.client

def list_usb_device_info():
    wmi = win32com.client.GetObject("winmgmts:")
    usb_devices = wmi.ExecQuery("SELECT * FROM Win32_USBHub")

    device_info = []
    for usb_device in usb_devices:
        device_id = usb_device.DeviceID
        drive_letters = get_drive_letters(device_id)
        
        device_info.append({
            "Nombre": usb_device.Name.strip(),
            "Descripción": usb_device.Description.strip(),
            "ID del Dispositivo": device_id,
            "Estado": usb_device.Status,
            "Letras de Unidad": ", ".join(drive_letters) if drive_letters else "No asignada",
            "Número de serie": usb_device.PNPDeviceID.split('\\')[-1],
        })

    return device_info

def get_drive_letters(device_id):
    wmi = win32com.client.GetObject("winmgmts:")
    partitions = wmi.ExecQuery(f"ASSOCIATORS OF {{Win32_PnPEntity.DeviceID='{device_id}'}} WHERE AssocClass=Win32_DiskDriveToDiskPartition")
    
    drive_letters = []
    for partition in partitions:
        logical_disks = wmi.ExecQuery(f"ASSOCIATORS OF {{Win32_DiskPartition.DeviceID='{partition.DeviceID}'}} WHERE AssocClass=Win32_LogicalDiskToPartition")
        for logical_disk in logical_disks:
            drive_letters.append(logical_disk.DeviceID)

    return drive_letters

if __name__ == "__main__":
    usb_device_info = list_usb_device_info()

    if usb_device_info:
        for idx, device in enumerate(usb_device_info, start=1):
            print(f"Dispositivo {idx}:")
            for key, value in device.items():
                print(f"  {key}: {value}")
            print("=" * 40)
    else:
        print("No se encontraron dispositivos USB conectados.")
