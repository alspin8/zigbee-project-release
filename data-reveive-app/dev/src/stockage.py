import csv
import itertools
from termcolor import colored
import os

class Stockage:

    def __init__(self, dir, headers:list, filename="data.csv"):
        self.path = f"{dir}/{filename}"
        self.fieldnames = headers
        try: 
            with open(self.path) : pass
        except IOError:
            self.initfile()

    def initfile(self):
        with open(self.path,'w',newline= '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()

    def writefile(self, data:list):
        if len(data) == len(self.fieldnames):
            to_write:dict
            with open(self.path,'a',newline= '') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, extrasaction='raise')
                for header, dt in itertools.zip_longest(self.fieldnames, data):
                    to_write[header] = dt
                try:
                    writer.writerow(to_write)
                except ValueError as exc :
                    raise ValueError(exc)
        else:
            raise exc from Exception('Inconsistent data')