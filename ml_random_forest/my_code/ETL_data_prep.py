from get_file_path_for_data import get_file_path_for_data
import pandas as pd
import numpy as np


def extract_transform_load_data(bool_start=False):
    #########################################################################
    # column names
    col_header_names_path = get_file_path_for_data(bool_var=True, folder_name='ref_data',
                                                   sub_folder_name=None, file_name='names.txt')
    # print("col_header_names_path=\n", col_header_names_path)
    # data file
    data_file_path = get_file_path_for_data(bool_var=True, folder_name='ref_data',
                                            sub_folder_name=None, file_name='autos.csv')
    # print("data_file_path=\n", data_file_path)
    #########################################################################
    # read list of column titles
    list_col_headers = []
    # opening the CSV file
    with open(col_header_names_path, mode='r') as file:
        # reading the CSV file
        text_file = pd.read_csv(file, sep=",")
        # print("text_file=\n",text_file)
        # displaying the contents of the CSV file
    list_col_headers = text_file.columns
    # print("list_col_headers= ", list_col_headers)
    #########################################################################
    # read data
    df = pd.read_csv(filepath_or_buffer=data_file_path,
                     sep=',',
                     header=None,
                     skip_blank_lines=True,
                     index_col=0,
                     skiprows=1)
    # drop first col from df
    df.reset_index(drop=True, inplace=True)
    # drop first col from list, row_id
    df.columns = list_col_headers[1:]
    # replace weird values
    df.replace(to_replace='?', value=np.nan, inplace=True)
    # drop na values, if any column has na, then drop entire row
    df.dropna(how='any', inplace=True)
    return df