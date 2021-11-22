import serial
import binascii

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
  ser = serial.Serial('/dev/ttyS0', 4800, bytesize=8, parity='N', stopbits=1, timeout=1)
  while ser:
    # ser.write('seb'.encode('ascii'))
    # msg = ser.read(19)
    # print(1, msg.hex())
    # ser.write('?r\r\n'.encode('ascii'))
    # msg = ser.read(19)
    # print(2, msg.hex())
    # print(ser.readline().decode('ascii', errors='replace'))
    # print(msg, msg.hex(), chr(int(msg.hex(), 16)), int(msg.hex(), 16))
    # print(bytearray.fromhex(ser.read(1).hex()).decode())
    # byte_array = bytearray.fromhex(msg.hex())
    # print(byte_array)
    # print(str(msg,'utf-8'))
    # binary_string = binascii.unhexlify(ser.read(19)[1:])
    # print(binary_string)
    # print(ser.read(19))
    hex_data = ser.read(19).hex()
    ascii_string = ''
    x = 0
    y = 2
    l = len(hex_data)
    while y <= l:
        ascii_string += chr(int(hex_data[x:y], 16))
        x += 2
        y += 2
    print (ascii_string)
except Exception as e:
  print(e)
  ser.close()