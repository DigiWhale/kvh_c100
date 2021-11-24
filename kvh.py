import serial
import time

class Kvh_Compass:
  def __init__(self, port):
    self.ser = serial.Serial(port, 4800, bytesize=8, parity='N', stopbits=1, timeout=1)
    # self.ser.write(b'h\r\n')
    self.ser.write(b's\r\n')
    self.ser.write(b'r,600\r\n')
    
  def set_msg_rate(self, rate):
    msg = b'=r,600\r'
    # msg = f'=r,{rate}\r'.encode()
    print(msg)
    self.ser.write(msg)
    print(self.ser.readline())
    print('Set rate to {}'.format(rate))
    
  def get_heading(self):
    self.ser.write(b'd0\r\n')
    nmea_sentence = self.ser.readline()
    # print(nmea_sentence)
    try:
      heading = nmea_sentence.split(b',')[1]
    except:
      self.ser.write(b'd0\r\n')
      nmea_sentence = self.ser.readline()
      heading = nmea_sentence.split(b',')[1]
    return float(heading.decode('utf-8'))
  
  def get_rate(self):
    self.ser.write(b'?r\r\n')
    raw_rate = self.ser.readline()
    rate = raw_rate.split(b' ')[1]. replace(b'\r', b'')
    return int(rate.decode('utf-8'))

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
  while True:
    # print(kvh_compass.get_heading())
    # time.sleep(1)
    # print(kvh_compass.get_rate())
    print(kvh_compass.ser.readline())