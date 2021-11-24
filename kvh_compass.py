import serial
import time
from adapters.redisAdapter import RedisAdapter
import geomag
import sys
from datetime import datetime

class Kvh_Compass:
  def __init__(self, port):
    self.ser = serial.Serial(port, 4800, bytesize=8, parity='N', stopbits=1, timeout=1)
    # self.ser.write(b's\r\n') #start automatic message transmission
    self.ser.write(b'=r600\r\n') #set message rate to 600/minute
    time.sleep(.2)
    self.ser.write(b'h\r\n') #stop automatic message transmission
    self.redis = RedisAdapter()
    self.heading = {'heading': 0}
    try:
      self.declination = geomag.declination(float(self.redis.get("msrs_lat")), float(self.redis.get("msrs_lng")))
    except:
      self.declination = geomag.declination(38.801744, -77.073058)
    try:
      self.redis.channel_client()
    except:
      print('Error: Redis connection failed')
      sys.exit()
    print(f'Declination: {self.declination}')
    time.sleep(.2)
    self.ser.write(b'=v,t\r\n') # turn on variation
    print("variation turned on ", self.ser.readline())
    time.sleep(.2)
    self.ser.write(b'?v\r\n') # variation active?
    print("variation active? ", self.ser.readline())
    time.sleep(.2)
    self.ser.write(f'=vd,{self.declination}\r\n'.encode()) # set variation
    print("variation set ", self.ser.readline())
    time.sleep(.2)
    self.ser.write(b'?vd\r') # read variation
    print("variation = ", self.ser.readline())
    
  def get_heading(self):
    self.ser.write(b'd0\r\n')
    nmea_sentence = self.ser.readline()
    try:
      heading = nmea_sentence.split(b',')[1]
    except:
      self.ser.write(b'd0\r\n')
      nmea_sentence = self.ser.readline()
      heading = nmea_sentence.split(b',')[1]
    self.heading['heading'] = float(heading.decode('utf-8'))
    return float(heading.decode('utf-8'))
  
  def publish_data_to_redis(self):
    object_data = {
        "sensor_type": 8,
        "sensor_value":{
            "kvh_heading": self.heading['heading'],                   
        },                
        "timestamp": datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S.%f')
    }
    try:
      self.redis.send_message('msrs_raspberry', object_data)
    except:
      print('Error: Redis connection failed')
      sys.exit()
  
if __name__ == '__main__':
  kvh_compass = Kvh_Compass('/dev/ttyS0')
  while True:
    print(kvh_compass.get_heading())
    kvh_compass.publish_data_to_redis()