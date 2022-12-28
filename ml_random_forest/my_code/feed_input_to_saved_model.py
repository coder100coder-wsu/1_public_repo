import pandas as pd
from get_file_path_for_data import get_file_path_for_data



def create_input_to_saved_model(bool_var=False,
                                folder_name='clean_etl_data_',
                                sub_folder_name='random_forest_regression',
                                file_name='clean_1.csv',
                                num_rows = 10):
    # get input_X
    data_file_path = get_file_path_for_data(bool_var=True,
                                            folder_name=folder_name,
                                            sub_folder_name=sub_folder_name,
                                            file_name=file_name)
    # print("data_file_path=\n", data_file_path)
    # read results_data. use as-is.
    # this is clean results_data, so expected that headers, missing, nan etc. already handled
    df = pd.read_csv(filepath_or_buffer=data_file_path)
    # print(df.head(3))
    # keep only a subset of all available columns that are also numericla datatype
    cols_to_keep = [
        ' length', ' width', ' height', ' curb-weight', ' engine-size',
        ' bore', ' stroke', ' compression-ratio', ' horsepower', ' peak-rpm', ' city-mpg',
        ' highway-mpg', ' price']
    df = df[cols_to_keep]
    # print(df.info())
    # print(df.columns)
    ##########################################################################################
    # declare predictors, drop target var from predictors
    X = df.drop([' price'], axis=1)
    return_subset_X = X[0:num_rows]

    return return_subset_X


# a = create_input_to_saved_model(bool_var=False,
#                                 folder_name='clean_etl_data_',
#                                 sub_folder_name='random_forest_regression',
#                                 file_name='clean_1.csv',
#                                 num_rows = 10)
# print(type(a))
# print(a)