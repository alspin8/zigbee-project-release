from digi.xbee.devices import XBeeDevice, XBeeException
from stockage import Stockage
from termcolor import colored
from serial.tools import list_ports
import time, serial

class DataRecovery(Stockage):

    BAUDRATE = 9600
    running = False

    def __init__(self):

        # Récupération du port sur lequel est branché le xbee
        PORT = self.get_port()

        # Définition du fichier de stockage de données
        dir = str(input("Enter data directory path : "))
        super().__init__(dir, ['date', 'heure', 'addr','data'])

        # Configuration de la carte réceptrice
        self.device = XBeeDevice(PORT, self.BAUDRATE)

        # Tentative de mise en écoute du device
        while not self.device.is_open():
            try:
                self.device.open()
                self.running = True
                self.logger("Device is open !",'green')

                #Ajout d'une fonction pour traiter les information envoyé par les cartes émétrices
                self.device.add_data_received_callback(self.my_data_received_callback)

            except serial.SerialException as exc:
                self.logger(exc,'red')
            except XBeeException as exc:
                self.logger(exc,'red')

            if not self.device.is_open():
                self.logger("Retry in 5 second !", 'yellow')
                time.sleep(5)

    def logger(self, msg, color):
        print(f"[{self.get_date()} {self.get_time()}] : " + colored(str(msg),color))

    def get_date(self):
        return time.strftime("%Y-%m-%d", time.localtime(time.time()))

    def get_time(self):
        return time.strftime("%H:%M:%S", time.localtime(time.time()))

    def get_port_by_scan(self):
        ports = list_ports.comports()
        for port, desc, hwid in sorted(ports):
            if desc.count("XBIB"):
                return port
        raise Exception("Xbee not find !") 

    def get_port(self):
        while True:
            choix = str(input("Set port manually ? y/n "))
            if choix.upper() == 'N':
                try:
                    return self.get_port_by_scan()
                except Exception as exc:
                    self.logger(exc, 'red')
                    exit()
            elif choix.upper() == 'Y':
                port = str(input('Enter port : '))
                return port

    def my_data_received_callback(self, xbee_message):
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data.decode("utf8")
        self.logger(f"Data received from {address} - {data}", 'green')
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