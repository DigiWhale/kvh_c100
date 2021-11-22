import serial

try:
  ser = serial.Serial('/dev/ttyS0', 4800, bytesize=8, parity='N', stopbits=1, timeout=1)
  heading = 0
  while ser:
    init_heading = int(ser.read(19).decode('utf-8').split(',')[1])
    if init_heading < 361:
      heading = init_heading
    print(heading)

except Exception as e:
  print(e)
  ser.close()