import pandas as pd
import numpy as np
from get_file_path_for_data import get_file_path_for_data
from save_output import save_output_predictions

qty_splits = 3
def split_big_df_into_many_small_df(bool_start=False):
    big_df_path = get_file_path_for_data(bool_var=True, folder_name='clean_etl_data_',
                                         sub_folder_name='random_forest_regression',
                                         file_name='clean_1.csv')
    # print("big_df_path=\n", big_df_path)
    # read clean data. use as-is.
    # this is clean results_data, so expected that headers, missing, nan etc. already handled
    df = pd.read_csv(filepath_or_buffer=big_df_path)
    shuffled = df.sample(frac=1.0)
    results = np.array_split(shuffled,qty_splits)
    counter_val = 0
    for df_partial in results:
        save_output_predictions(input_df=df_partial,
                                output_dir_name='clean_etl_data_',
                                output_sub_dir_name='random_forest_regression',
                                counter=counter_val,
                                input_index_label='row_index',
                                file_prefix='clean_part_')
        counter_val += 1

    return 1



split_big_df_into_many_small_df(bool_start=True)