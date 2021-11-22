import serial

try:
  ser = serial.Serial('/dev/ttyS0', 4800, bytesize=8, parity='N', stopbits=1, timeout=1)
  while ser:
    # msg = bytearray([100, 48, 13])
    msg = bytearray([104, 13])
    ser.write(msg)
    hex_data = ser.read(19).hex()
    print('hex_data', hex_data)
    ascii_string = ''
    x = 0
    y = 2
    l = len(hex_data)
    while y <= l:
        ascii_string += chr(int(hex_data[x:y], 16))
        x += 2
        y += 2
    print ("ascii_string", ascii_string)
except Exception as e:
  print(e)
  ser.close()