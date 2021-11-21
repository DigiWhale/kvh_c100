import serial 

try:
  with serial.Serial('/dev/ttyS0', 9600, timeout=1) as ser:
    print(ser.readline().decode('utf-8'))
except Exception as e:
  print(e)
  ser.close()