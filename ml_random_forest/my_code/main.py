from setup_pkgs import setup_packages
from make_output_dir import make_output_dir
from required_pkgs import required_packages
from ETL_data_prep import extract_transform_load_data
from save_output import save_output_predictions
from random_forest_regression import run_random_forest_regression

required_pkgs = required_packages(bool_start=True)
# run once to setup required packages in virtual_env
counter_input = 1
while counter_input == 1:
    return_val = setup_packages(counter=counter_input,
                                bool_var=True,
                                required_pkgs=required_pkgs)
    if return_val == 1:
        counter_input = 0
        # create output dir
        make_output_dir(sub_dir_name='random_forest_regression',
                        output_dir_name='output_predictions')
        # ETL data
        df_clean = extract_transform_load_data(bool_start=True)
        # create dir for storing clean data
        make_output_dir(sub_dir_name='random_forest_regression',
                        output_dir_name='clean_etl_data')
        # save ETL/clean data to file
        save_output_predictions(input_df=df_clean,
                                output_dir_name='clean_etl_data_',
                                output_sub_dir_name='random_forest_regression',
                                counter=1,
                                input_index_label='row_index',
                                file_prefix='clean_')

        run_random_forest_regression(bool_var=False,
                                     clean_csv_data_file_name='clean_1.csv',
                                     data_in_folder_name='clean_etl_data_')

    if counter_input == 0:
        break
