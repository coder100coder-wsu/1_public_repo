import os
from pathlib import Path

dir_name_dict = {'main_dir':'my_dir',
                 'sub_dir':['ml_config','ml_models','ml_results','prog_logging','ref_data',
                            'clean_data']
                }

def create_dir_structure(bool_start=False):
    """
    creates directory structure for running ML-Ops
    :param bool_start: set to True to run the func
    :return: 1
    """
    if bool_start:
        # get the path_from_func of the current directory
        path_from_func = get_current_dir(bool_start=True)
        path_from_func = Path(path_from_func)
        print("Path of the current directory : \n", path_from_func)
        dir_list = get_dir_list(bool_start=True, path=path_from_func)
        # print("dir_list= \n", dir_list)
        if not dir_name_dict['main_dir'] in dir_list:
            make_new_dir(bool_start=True, parent_dir=path_from_func,
                         new_dir_name=dir_name_dict['main_dir'], create=1)
        # check_if_dir_exists(bool_start=True,
        #                     dir_name=dir_name_dict['main_dir']
        #                     parent_dir=path_from_func)
        # if path_from_func:
        #     # parent_dir_path = go_up_given_levels_dir(bool_start=True, path_arg=path_from_func,
        #     #                                          go_up_levels=1)
        #
        #     for root, dirs, files in os.walk(path_from_func):
        #         print("root= \n", root)
        #         print("parent_dir_path= \n", path_from_func)
        #
        #         if root == path_from_func:
        #             for name in files:
        #                 print("name= ", name)
        #         print("dirs= ",[(dir, "::", len(dir)) for dir in dirs if len(dirs)!=0])
        #     # print("root= \n", root_s)
        #     # print("dirs= \n", dirs_s)
        #     # print("files= \n", files_s)
        #
        #         # for name in files:
        #             # if name.endswith(("lib", ".so")):
        #             #     os.path.join(root, name)
        #
        #
        #     # try:
        #     #     os.mkdir(path)
        #     # except OSError as error:
        #     #     print(error)

        # # get the name of the current directory
        # repn = get_basename(bool_start=True, path=path_from_func)
        # print("Name of the current directory : \n" + repn)
        # # get the script path_from_func
        # path_from_func = get_full_path(bool_start=True)
        # print("The script path_from_func is : \n" + path_from_func)
        return 1
    else:
        return -1


def get_current_dir(bool_start=False):
    if bool_start:
        current_dir_path = os.getcwd()
        return current_dir_path
    else:
        return -1


def get_basename(bool_start=False, path=None):
    if bool_start and path is not None:
        basename = os.path.basename(path)
        return basename
    else:
        return -1


def get_full_path(bool_start=False):
    if bool_start:
        full_path = os.path.realpath(__file__)
        return full_path
    else:
        return -1


def go_up_given_levels_dir(bool_start=False, path_arg=None, go_up_levels=1):
    if bool_start and path_arg is not None:
        # go up one level
        levels_up = go_up_levels
        dir_path_at_levels_above = path_arg.parents[levels_up - 1]
        print("dir_name_at_{}_levels_above= \n{}".format(levels_up, dir_path_at_levels_above))
        return dir_path_at_levels_above
    else:
        return -1

def get_dir_list(bool_start=False, path=None):
    if bool_start and path is not None:
        dir_list= os.listdir(path)
        print("dir_list= \n", (dir_list,":",[type(dir) for dir in dir_list]))
        return dir_list
    else:
        return -1


def make_new_dir(bool_start=False, parent_dir=None, new_dir_name=None, create=1):
    if bool_start and parent_dir is not None and new_dir_name is not None and create==1:
        try:
            new_dir_path = os.path.join(parent_dir, new_dir_name)
            print("new_dir_path= \n", new_dir_path)
            return new_dir_path
        except OSError as error:
            print(error)
    else:
        return -1


def check_if_dir_exists(bool_start=False, dir_name=None):
    if bool_start and dir_name is not None:
        full_path = os.path.realpath(__file__)
        return full_path
    else:
        return -1


create_dir_structure(bool_start=True)