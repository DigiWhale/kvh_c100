import os
import socket
from redis.client import PubSub
import requests
import time
import json
import redis

class RedisAdapter():

    __server_ip = ''
    __server_port = 6379
    __database = 0
    __pass = 'Redis2019!'
    __verbose = False
    __redisConn = None

    def __init__(self, database = 0, port = 6379, verbose = False):
        """
        Class to work as an adapter to the Redis cache database, by using a config.json file it is possible to set the server connection and port of communication
        """
        f = open('/home/pi/MSRS-RPI/config.json')
        json_config = json.loads(f.read())  
        server = json_config['server']
        hostname = server['local'] if server['use_local'] == True else server['remote'] 
        backupip = socket.gethostbyname(hostname)

        self.__database = database
        self.__verbose = verbose     
        self.__server_ip = str(os.environ.get('msrsip')) if os.environ.get('msrsip') != None else str(backupip)   
        self.__redisConn = redis.StrictRedis(host=self.__server_ip, port=self.__server_port, db=self.__database, password=self.__pass)
        # result = None
        # while result is None:
        #     try:
        #         self.__redisConn = redis.StrictRedis(host=self.__server_ip, port=self.__server_port, db=self.__database, password=self.__pass)
        #         result = True
        #     except:
        #         pass             

    def __RequestException(self, e):
        """
        Right now on exceptions we are making the software wait, but we can implement the logic later here
        """
        print(e)

    def set(self, object):
        """
        This is the common set function from Redis, you must pass an object on the format { 'key': value }
        """
        try:
                       
            self.__redisConn.mset(object) # key: value
            if(self.__verbose):
                print('Data Sent', object)
            
        except Exception as e:            
            self.__RequestException(e)

    def get(self, key):
        """
        This is the common mget from Redis, but it already get the first element of the array and decode it from bytes to str, so it is necessary to apply the conversion when another format
        """
        try:
            
            value = self.__redisConn.mget(key)
            if(self.__verbose):
                print('Data Read', value[0].decode())

            return value[0].decode() if value[0] != None else None

        except Exception as e:
            self.__RequestException(e)


    def push(self, collection, key):
        """
        This is the common lpush from Redis, send an object that will be dumped into the collection
        """
        try:

            self.__redisConn.rpush(collection, json.dumps(key))
            self.__redisConn.expire(collection, 2)

            if(self.__verbose):
                print('Data Pushed to the collection {collection}'.format(collection=collection) )

        except Exception as e:
            self.__RequestException(e)

    def pop(self, collection):
        """
        This is the common lpush from Redis
        """
        try:
            
            value = self.__redisConn.lpop(collection) if self.__redisConn.llen(collection) else None
            to_json = json.loads(value.decode()) if value != None else {}

            if(self.__verbose):
                print('{data} popped out of the collection {collection}'.format(collection=collection, data = value) )

            return to_json

        except Exception as e:
            self.__RequestException(e)

    def channel_server(self, channel_name):
        """
        Method to open and subscribe to a channel
        """
        p = self.__redisConn.pubsub()
        p.subscribe(channel_name)

        return p

    def channel_client(self):
        """
        Open a client channel communication
        """
        self.__redisConn.pubsub(ignore_subscribe_messages=True)
    
    def read_message(self, subscription: PubSub):
        """
        Read the subcribed  members on this pub sub
        """        
        message = subscription.get_message()

        if message:

            is_byte = type(message['data']) != type(0)

            if is_byte:

                byte_data = message['data']
                utf_8_data = byte_data.decode('UTF-8')
                to_json = json.loads(utf_8_data)

                return to_json
        else:
            return None

    def send_message(self, channel = '', message = None):
        """
        Send Message to an open Channel, this method will always convert the object to a json.dumps string
        """
        self.__redisConn.publish(channel, json.dumps(message))