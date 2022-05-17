from digi.xbee.devices import XBeeDevice, XBeeException
from digi.xbee.models.address import XBee64BitAddress
from serial import SerialException
from stockage import Stockage
from termcolor import colored
import os, time

class DataRecovery(Stockage):

    PORT = "usbserial-1130"
    BAUDRATE = 9600
    running = False

    def __init__(self):
        
        # Définition du fichier de stockage de données
        dir = str(input("Enter data directory path : "))
        super().__init__(dir, ['date', 'heure', 'addr','data'])

        # Configuration de la carte réceptrice
        self.device = XBeeDevice(self.PORT, self.BAUDRATE)

        # Tentative de mise en écoute du device
        while not self.device.is_open():
            try:
                self.device.open()
                self.running = True
                self.logger("Device is open !",'green')

                #Ajout d'une fonction pour traiter les information envoyé par les cartes émétrices
                self.device.add_data_received_callback(self.my_data_received_callback)

            except SerialException as exc:
                self.logger(exc,'red')
            except XBeeException as exc:
                self.logger(exc,'red')

            self.logger("Retry in 5 second !", 'yellow')
            time.sleep(5)

    def logger(self, msg, color):
        print(f"[{self.get_date()} {self.get_time()}] : " + colored(str(msg),color))

    def get_date(self):
        return time.strftime("%Y-%m-%d", time.localtime(time.time()))

    def get_time(self):
        return time.strftime("%H:%M:%S", time.localtime(time.time()))

    def my_data_received_callback(self, xbee_message):
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data.decode("utf8")
        self.logger("Data received from {adress} - {data}", 'green')
        try:
            self.writefile([self.get_date(), self.get_time(), address, data])
        except ValueError as exc:
            self.logger(exc,'yellow')
        except Exception as exc:
            self.logger(exc,'yellow')

    def run(self):
        if self.running:
            self.logger("Listenning...",'green')
            while self.running:
                if not self.device.is_open():
                    self.running = False
            self.logger("Closing device !",'yellow')
            self.device.close()