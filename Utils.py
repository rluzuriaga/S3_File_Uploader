import os
from typing import List

def get_folders_to_create_in_bucket(path_to_walk) -> List[str]:
    main_folder_name = path_to_walk[path_to_walk.rfind('/') + 1:]
    list_of_folders_to_create = []

    for dirpath, dirnames, filenames in os.walk(path_to_walk):
        list_of_folders_to_create.append(main_folder_name + dirpath.split(main_folder_name)[-1])
    
    return list_of_folders_to_create
