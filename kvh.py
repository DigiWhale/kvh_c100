import serial 

with serial.Serial('/dev/ttyS1', 19200, timeout=1) as ser:
  print(ser.readline().decode('utf-8'))