#!/usr/bin/env python
import os

def except_notify_exit(e):
    os.system(f"notify-send \"nm_chooser.py {e}\"")
    raise e
    exit(0)


try:
    import sdbus
    from sdbus_block.networkmanager import (
        NetworkDeviceGeneric,
        NetworkDeviceWireless,
        NetworkManagerDeviceInterface,
        NetworkManager,
        NetworkConnectionSettings,
        AccessPoint,
        DeviceType,
    )
except ModuleNotFoundError as e:
    except_notify_exit(e)
    
def main():
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    network_manager = NetworkManager()
    all_devices = {path: NetworkDeviceGeneric(path) for path in network_manager.devices}
    wifi_devices = [
        NetworkDeviceWireless(path)
        for path, device in all_devices.items()
        if device.device_type == DeviceType.WIFI
    ]
    for i in wifi_devices:
        for j in i.access_points:
            c = AccessPoint(j)
            print(c.ssid.decode())
            i.request_scan(j)

        #print(i.access_points)
        # c = AccessPoint(i.access_points)
        # print(c.ssid())

    # Get active connections

if __name__ == "__main__":
    main()
