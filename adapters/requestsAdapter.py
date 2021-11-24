import os
import socket
import requests
import time
import json

class RequestAdapter():

    __protocol = 'http://'
    __server_ip = ''
    __server_port = 8000
    __auth = ('admin','admin')
    __verbose = False
    
    def __init__(self, port = 8000, verbose = False):
        f = open('/home/pi/MSRS_RPI/config.json')
        json_config = json.loads(f.read())  
        server = json_config['server']
        hostname = server['local'] if server['use_local'] == True else server['remote'] #'localhost' #socket.gethostname()
        backupip = socket.gethostbyname(hostname)   
        self.__verbose = verbose     
        self.__server_ip = str(os.environ.get('msrsip')) if os.environ.get('msrsip') != None else str(backupip)        

    def __mount_url(self, api):
        return self.__protocol + self.__server_ip + ':' + str(self.__server_port) + '/' + api

    def __RequestException(self, e):
        """
        Handle the exceptions in the rigth way
        """
        # print('Exception:', str(e))
        time.sleep(1)

    def post(self, api, params):
        """
        Post request to the Server API
        """
        try:
            endpoint = self.__mount_url(api)
            r = requests.post(endpoint, json = params, auth=self.__auth)         
            # print(self.__verbose)
            if(self.__verbose):
                print('Data Sent', params, r)
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            self.__RequestException(e)
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            self.__RequestException(e)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            self.__RequestException(e)

    def get(self, api):
        """
        Request Get API
        """
        try:
            endpoint = self.__mount_url(api)
            r = requests.get(endpoint, auth=self.__auth)

            if(self.__verbose):
                print('Data Sent', r)

            return r

        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            self.__RequestException(e)
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            self.__RequestException(e)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            self.__RequestException(e)