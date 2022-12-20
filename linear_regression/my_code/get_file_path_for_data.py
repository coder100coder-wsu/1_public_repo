from pathlib import Path
import os


def get_file_path_for_data(folder_name='ref_data', file_name='autos.csv', bool_var=False):
    """
    This function returns data_file_path.
    :param bool_var: executes func if True
    :return: data_file_path: constructed file path for data file
    """
    # locate data to be processsed
    current_file_path = Path(__file__).parent
    # print(current_file_path)
    # go up one dir in folder structure
    dir_path = os.path.dirname(current_file_path)
    # print(dir_path)
    # construct data file path
    data_file_path = dir_path + '\\' + folder_name + '\\' + file_name
    # print(data_file_path)
    return data_file_path

