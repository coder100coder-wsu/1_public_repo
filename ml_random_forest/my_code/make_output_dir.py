from pathlib import Path
import os


def make_output_dir(sub_dir_name='ml_algo_name_here',
                    output_dir_name='output_predictions'):
    """
    function creates output directory
    :param sub_dir_name: existing target/root dir where the output dir should be created
    :param output_dir_name: specify dir_name if other than default
    :return: full path for newly created dir
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # print("script_dir= ", script_dir)
    # go up one dir in folder structure
    up_one_level_dir_path = os.path.dirname(script_dir)
    # print("up_one_level_dir_path= ", up_one_level_dir_path)
    base_file_name = os.path.basename(sub_dir_name)
    # print("base_file_name= ", base_file_name)
    # extract file_name without extension
    base_file_name_no_extension = base_file_name.split('.')[0]
    # print("base_file_name_no_extension= ", base_file_name_no_extension)
    # print("script_dir = ", script_dir)
    # construct new folder name
    new_folder_name = output_dir_name + '_' + "/" + str(base_file_name_no_extension)
    # print("new_folder_name= ", new_folder_name)
    # Construct full path for output dir
    dest_dir = os.path.join(up_one_level_dir_path, new_folder_name)
    # print("dest_dir = ", dest_dir)
    try:
        os.makedirs(dest_dir)
    except OSError:
        # print("Dir already exists!")
        # pass  # dir already exists
        return -1
    return dest_dir


# make_output_dir(sub_dir_name='random_forest_regression', output_dir_name='output_predictions')