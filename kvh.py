import serial 

with serial.Serial('/dev/ttyS0', 9600, timeout=1) as ser:
  print(ser.readline().decode('utf-8'))