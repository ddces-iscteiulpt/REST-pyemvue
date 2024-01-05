import json
import datetime
import logging
from pyemvue.enums import Scale, Unit

def data_devices_status(vue_login):
    try:
        devices = vue_login.get_devices()  # Get the devices
        device_info = {}  # Dictionary to store device information
        for device in devices:
            if device.device_gid not in device_info:
                device_info[device.device_gid] = device
            else:
                device_info[device.device_gid].channels += device.channels

        devices_data = doc_recursive(device_info)
        print(devices_data)
        return devices_data
    except Exception as e:
        logging.error(f"Error occurred in get_all_devices_status: {str(e)}")
        return None

def doc_recursive(list_device, depth=0):
    try:
        device_data = []  # List to store device data
        for gid, device in list_device.items():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Hardcoded timestamp as current time
            data = {
                'gid': gid,
                'device_name': device.device_name,
                'manufacturer_id': device.manufacturer_id,
                'model': device.model,
                'firmware': device.firmware,
                'parent_device_gid': device.parent_device_gid,
                'parent_channel_num': device.parent_channel_num,
                'status': device.connected,
                'timestamp': timestamp,
            }
            if not device.connected:
                data['offline_since'] = device.offline_since.strftime('%Y-%m-%d %H:%M:%S')
            device_data.append(data)

        devices_data = json.dumps(device_data, indent=4)
        return devices_data
    except Exception as e:
        logging.error(f"Error occurred in doc_recursive: {str(e)}")
        return None