from pathlib import Path
import os

import pandas as pd


def save_output_predictions(input_df,
                            output_dir_name='output_predictions_',
                            output_sub_dir_name = 'linear_regression',
                            counter=1,
                            input_index_label='row_index',
                            file_prefix= 'run_'):
    """
    function creates output directory
    :param input_df: df to be saved
    :param output_dir_name: specify dir_name if other than default
    :return: 1 if successful, (-1) if not
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # print("script_dir= ", script_dir)
    # go up one dir in folder structure
    up_one_level_dir_path = os.path.dirname(script_dir)
    # print("up_one_level_dir_path= ", up_one_level_dir_path)
    root = up_one_level_dir_path
    dirlist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
    # print("dirlist=\n", dirlist)
    if output_dir_name in dirlist:
        output_file_dir_path = up_one_level_dir_path + "\\" \
                               + output_dir_name + "\\" \
                               + output_sub_dir_name + "\\"
        # print("output_file_dir_path=\n", output_file_dir_path)
        output_file_name = file_prefix + str(counter) + ".csv"
        # print("output_file_name=\n", output_file_name)
        output_file_path = output_file_dir_path + output_file_name
        # print("output_file_path=\n", output_file_path)
        # write df
        input_df.to_csv(path_or_buf=output_file_path,
                        sep=",",
                        header=True,
                        index=True,
                        index_label=input_index_label,
                        mode='w')
        return 1
    else:
        print("save_output function; output_dir_name not found in current dir structure.")
        return -1



# data = {'Name':['Tom', 'nick', 'krish', 'jack'], 'Age':[20, 21, 19, 18]}
# df_sample= pd.DataFrame(data)
# save_output_predictions(input_df=df_sample, output_dir_name='output_predictions_')