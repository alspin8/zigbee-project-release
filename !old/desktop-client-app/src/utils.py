from os import walk
import json, logging, csv, itertools

class FileUtils:

    @staticmethod
    def get_dict_from_jsonfile(file):
        with open(file) as json_data:
            data_json = json.load(json_data)
        data_str = json.dumps(data_json)
        return json.loads(data_str) 

    @staticmethod
    def write_jsonfile_from_dict(file, dict):
        with open(file, 'w') as json_data:
            return json.dump(dict, json_data)

    @staticmethod
    def list_file(path):
        files = []
        for dir, subdir, file in walk(path):
            files.extend(file)
        return files

    @staticmethod
    def set_csv_header(file, headers):
         with open(file, 'w') as csv_file:
             obj = csv.DictWriter(csv_file, fieldnames=headers)
             obj.writeheader()

    @staticmethod
    def write_csv_row(file, headers:list, dict:list):
        with open(file, 'a') as csv_file:
            obj = csv.DictWriter(csv_file, fieldnames=headers)
            obj.writerow({k: v for k,v in itertools.zip_longest(headers, dict)})
    
    @staticmethod
    def get_csv_list(file, date):
        global_lst = []
        with open(file, 'r') as csv_file:
            obj = csv.DictReader(csv_file)
            for i in obj:
                lst = []
                if i['date'] == date:
                    for key, value in i.items():
                        lst.append(value)
                global_lst.append(lst)
        return global_lst


            

def date_format(date): return(f"Le {date.replace(date[0:10], f'{date[8:10]}/{date[5:7]}/{date[0:4]}')[0:10]}"
                              f" à {date[12:len(date) - 1]}"
                            )

def get_png_file_name(path): 
    lst = path.split('/')
    return lst[len(lst) - 1].replace('.png', '')   
                                

class Logger:

    def __init__(self, level=logging.INFO) -> None:
        logging.basicConfig(filename = "../logs/logs.log",      
                            filemode = "a",
                            format = "%(levelname)s %(asctime)s - %(message)s",
                            level = level)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(level)

    def get_logger(self): return self.__logger       