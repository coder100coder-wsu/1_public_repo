from setup_pkgs import setup_packages
from make_output_dir import make_output_dir

required_pkgs = {'pandas', 'numpy', 'scikit-learn', 'statsmodels',
                 'Path','os'}

# run once to setup required packages in virtual_env
counter_input = 1
while counter_input == 1:
    return_val = setup_packages(counter=counter_input,
                                bool_var=True,
                                required_pkgs=required_pkgs)
    if return_val == 1:
        counter_input = 0
        # create output dir
        make_output_dir(input_path= 'linear_regression',
                        output_dir_name='output_predictions')
        # import necessary function from relevant file
        from linear_regression import run_linear_reg
        run_linear_reg(bool_var=True,
                       column_titles='names.txt',
                        csv_data_file_name = 'autos.csv',
                        data_in_folder_name = 'ref_data'
        )

    if counter_input == 0:
        break
