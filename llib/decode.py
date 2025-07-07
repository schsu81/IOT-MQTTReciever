import struct,base64
# Define the struct format to unpack the entire byte array
_main_struct_format = '<2H1I16sf8s36s4s16s'  # Little-endian: 2 unsigned 16-bit ints, 1 unsigned 32-bit int, 8-byte string, float, 40-byte string, 4-byte string, 16-byte string
_louver_format = '<6s10s4H3f'
_wind_format = '<2H'
_gnss_format = '<3f4s'
# %% ==========================================================================================
# Format MAC address to ASCII
def format_mac_address_as_ascii(mac_bytes):
    try:
        return ''.join(chr(byte) for byte in mac_bytes)
    except ValueError:
        return mac_bytes.hex()

# Decode and parse sensor data    
def decode_and_parse_sensor_data(encoded_data):
    """
    Decodes a Base64 encoded string, checks the type and id from the initial bytes,
    and unpacks the remaining data according to the predefined struct format for sensor data.

    :param encoded_data: str - Base64 encoded string containing binary sensor data
    :return: dict or str - Dictionary containing parsed sensor data or an error message
    """
    #global main_struct_format,louver_format,wind_format,gnss_format
    #from __main__ import main_struct_format,louver_format,wind_format,gnss_format
    # Decode the Base64 string to bytes
    decoded_bytes = base64.b64decode(encoded_data)
    # print("decoded_bytes:", decoded_bytes)

    
    # Check if we have enough data to unpack
    if len(decoded_bytes) >= struct.calcsize(_main_struct_format):
        unpacked_data = struct.unpack(_main_struct_format, decoded_bytes)
        # Unpack louver_data
        louver_data = struct.unpack(_louver_format, unpacked_data[6])
        # Unpack wind_data
        wind_data = struct.unpack(_wind_format, unpacked_data[7])
        # Unpack gnss_data
        gnss_data = struct.unpack(_gnss_format, unpacked_data[8])

        station_name_bytes = unpacked_data[5]  # 假設 `station_name` 在索引 5
        station_name = station_name_bytes.decode('utf-8').strip('\x00')  # 解碼並移除填充字符
        # Create a dictionary with the data, mapping each field to a meaningful name
        data_dict = {
            "type": unpacked_data[0],
            "id": unpacked_data[1],
            "timestamp": unpacked_data[2],
            "station_mac": format_mac_address_as_ascii(unpacked_data[3]),
            "voltage": unpacked_data[4],
            "station_name": station_name,
            "louver_mac": louver_data[0].hex(),
            "louver_reserved": louver_data[1].hex(),
            "pm2p5": louver_data[2],
            "pm10": louver_data[3],
            "co2": louver_data[4],
            "humidity": louver_data[5],
            "hdc1080_temperature": louver_data[6],
            "dsp310_temperature": louver_data[7],
            "airPressure": louver_data[8],
            "windSpeed": wind_data[0],
            "windDirection": wind_data[1],
            "latitude": gnss_data[0],
            "longitude": gnss_data[1],
            "altitude": gnss_data[2],
            "gnss_reserved": gnss_data[3].hex()
        }
        return data_dict
    else:
        error_msg = "Error: Data length mismatch. Expected at least {} bytes, got {} bytes.".format(
            struct.calcsize(_main_struct_format), len(decoded_bytes))
        print(error_msg)
        return {"error": error_msg}
# %% ==========================================================================================