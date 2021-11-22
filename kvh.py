import serial

try:
  ser = serial.Serial('/dev/ttyS0', 4800, bytesize=8, parity='N', stopbits=1, timeout=1)
  while ser:
    print(ser.read(19).decode('utf-8'))
    # byte = ser.read(1)
    # hex = byte.hex()
    # integer = int(hex, 16)
    # string = chr(integer)
    # print("byte", byte, "hex", hex, "integer", integer, "string", string)
except Exception as e:
  print(e)
  ser.close()