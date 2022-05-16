from digi.xbee.devices import XBeeDevice, XBeeException
from serial import SerialException
from stockage import Stockage
from termcolor import colored
import os, time
from digi.xbee.models.address import XBee16BitAddress

class DataRecovery(Stockage):

    PORT = "COM4"
    BAUDRATE = 9600
    running = False

    def __init__(self):
        super().__init__()
        os.system('color')
        #Configuration de la carte réceptrice
        self.device = XBeeDevice(self.PORT, self.BAUDRATE)
        #Tentative de mise en écoute du device
        try:
            self.device.open()
            self.running = True
            self.logger("Device is open !",'green')
            #Ajout d'une fonction pour traiter les information envoyé par les cartes émétrices
            self.device.add_data_received_callback(self.my_io_sample_received_callback)
        except SerialException as exc:
            self.logger(exc,'red')
        except XBeeException as exc:
            self.logger(exc,'red')
        # finally:
        #     if self.device is not None and self.device.is_open():
        #         self.logger("Closing device !",'green')
        #         self.device.close()

    def logger(self, msg, color):
        print(f"[{self.get_date()} {self.get_time()}] : " + colored(str(msg),color))

    def get_date(self):
        return time.strftime("%Y-%m-%d", time.localtime(time.time()))

    def get_time(self):
        return time.strftime("%H:%M:%S", time.localtime(time.time()))

    def my_io_sample_received_callback(self, xbee_message):
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data.decode("utf8")
        data = data[:len(data)-2]
        # if remote.get_16bit_addr() == XBee16BitAddress(bytearray(['0','F','F','F'])):
        filename = 'D098.csv'
        # else:
        #     print(type(remote.get_16bit_addr()))
        # self.logger(f"Adresse {remote.get_16bit_addr()} inconnue", 'green')
        try:
            self.writefile(filename, self.get_date(), self.get_time(), address, data)
        except ValueError as exc:
            self.logger(exc,'orange')
        print("Data received from %s - %s" % (address, data))

    def run(self):
        if self.running:
            self.logger("Listenning...",'green')
            while self.running:
                if not self.device.is_open():
                    self.running = False
            self.logger("Closing device !",'orange')
            self.device.close()