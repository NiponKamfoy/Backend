import os
from app.config import Config
from os import path

basepath = path.dirname(__file__)
#get name of index in folder
folder_data = path.abspath(path.join(basepath, "..", "data"))
config_data = Config() 
# folder_data = config_data['data_index_path']
dir_list2 = os.listdir(folder_data)
### create file each province
def get_list_data():
    meta_data = {}
    for data_provider in dir_list2:
        folder_data_provider = rf"{folder_data}/{data_provider}" # path of data 
        meta_data[data_provider] = {}
        dir_list3 = os.listdir(folder_data_provider)
        for index_type in dir_list3 :
            folder_index_type = rf"{folder_data}/{data_provider}/{index_type}" # path of data 
            dir_list4 = os.listdir(folder_index_type)
            meta_data[data_provider][index_type] = {}
            for index_name in dir_list4 :
                folder_index_name = rf"{folder_data}/{data_provider}/{index_type}/{index_name}" # path of data 
                dir_list5 = os.listdir(folder_index_name)
                meta_data[data_provider][index_type][index_name] = dir_list5
    return meta_data



