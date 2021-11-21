import serial

def readline(ser):
    eol = b'\r'
    leneol = len(eol)
    line = bytearray()
    while True:
        c = ser.read(1)
        print(c)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line) 

try:
  ser = serial.Serial('/dev/ttyS0', 4800, timeout=1)
  while ser:
    # ser.write(b'd0\r')
    print(ser.read(19).decode('utf-8'))
except Exception as e:
  print(e)
  ser.close()