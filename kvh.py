import serial 

try:
  ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
  while ser:
    print(ser.read(19).decode('utf-8'))
except Exception as e:
  print(e)
  ser.close()