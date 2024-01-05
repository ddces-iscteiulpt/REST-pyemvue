import json
from time import process_time_ns
from pyemvue.enums import Scale, Unit


def data_instant_measures(vue_login, gid, instant, scale, unit=Unit.KWH.value):
    scale_mapping = {
        'S': Scale.SECOND.value, 
        'M': Scale.MINUTE.value,  # Default scale value
        'H': Scale.HOUR.value,
        'd': Scale.DAY.value,
        'm': Scale.MONTH.value,
        'Y': Scale.YEAR.value
    }
    scale = scale_mapping.get(scale, None)
    if scale is None:
        scale = Scale.MINUTE.value
        pass
    
    devices = vue_login.get_devices()   # Get the devices
    if not devices:
        return json.dumps({"error": "No devices found"}, indent=4)
    
    for device in devices:
        if device.device_gid == gid:
            gid = device.device_gid
            try:
                usage = vue_login.get_device_list_usage(
                    [gid],
                    instant,
                    scale=scale,
                    unit=unit)
            except Exception as e:
                return json.dumps({"error": str(e)}, indent=4)
            
            channels_data = {}       # Dictionary to store channel data
            for channel in usage[gid].channels:
                channel_data = usage[gid].channels[channel]
                channels_data[channel_data.channel_num] = {
                    'channel_num': channel_data.channel_num,
                    'channel_name': channel_data.name,
                    'usage': channel_data.usage,
                    'percentage': channel_data.percentage,
                    'timestamp': channel_data.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            device_data = {
                'gid': gid,
                'instant': instant.strftime('%Y-%m-%d %H:%M:%S.%f'),
                'scale': scale,
                'device_name': device.device_name,
                'status': device.connected,
                'channels': channels_data,
            }
            return json.dumps(device_data, indent=4)

    return json.dumps({"error": f"No device found with gid {gid}"}, indent=4)