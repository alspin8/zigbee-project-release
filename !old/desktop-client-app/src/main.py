from mainwindow import MainWindow
from utils import FileUtils
import datetime

def foo():
    dct = dict()
    FileUtils.set_csv_header(f'../../data/D092.csv', ['date', 'heure', 'salle', 'température'])
    for k in range(30):
            FileUtils.write_csv_row(f'../../data/D092.csv', ['date', 'heure', 'salle', 'température'], ['2022-03-15', '12H34', 'D098', k])

if __name__ == '__main__':
    # foo()
    w = MainWindow()
    w.run()

    # print(FileUtils.get_csv_list('../../data/D092.csv', '2022-03-15'))



    

