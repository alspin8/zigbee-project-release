import csv
from termcolor import colored
import os

class Stockage:

    __fieldnames = ['date', 'heure', 'adrr','data']

    def __init__(self, filenames = []):
        for filename in filenames:
            try: 
                with open(f"../data/{filename}") : pass
            except IOError:
                self.initfile(filename)

    def initfile(self, filename):
        with open(f"../data/{filename}",'w',newline= '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.__fieldnames)
            writer.writeheader()

    def writefile(self, filename, date, heure, adrr, data):
        with open(f"../../data/{filename}",'a',newline= '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.__fieldnames, extrasaction='raise')
            try:
                writer.writerow({'date' : date, 'heure': heure, 'adrr': adrr, 'data': data})
            except ValueError as exc :
                raise ValueError(exc)