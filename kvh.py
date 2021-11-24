import serial
import time

class Kvh_Compass:
  def __init__(self, port):
    self.ser = serial.Serial(port, 4800, bytesize=8, parity='N', stopbits=1, timeout=1)
    self.ser.write(b'h\r\n')
    
  def get_heading(self):
    self.ser.write(b'd0\r\n')
    nmea_sentence = self.ser.readline()
    return nmea_sentence

# try:
#   ser = serial.Serial('/dev/ttyS0', 4800, bytesize=8, parity='N', stopbits=1, timeout=1)
#   heading = 0
#   while ser:
#     # init_heading = float(ser.read(19).decode('utf-8').split(',')[1])
#     # if init_heading < 361:
#     #   heading = init_heading
#     # print(heading)
#     ser.write(b'?w\r\n')
#     print(ser.readline())

# except Exception as e:
#   print(e)
#   ser.close()
  
if __name__ == '__main__':
  kvh_compass = Kvh_Compass('/dev/ttyS0')
  print(kvh_compass.get_heading())
  time.sleep(1)
  while True:
    kvh_compass.ser.readline()