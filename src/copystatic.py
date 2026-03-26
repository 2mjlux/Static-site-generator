import os
import shutil

def copystatic(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    files_to_copy = os.listdir(source)
    for file in files_to_copy:
        filepath = os.path.join(source, str(file))
        file_destination = os.path.join(destination, str(file))
        if os.path.isfile(filepath):
            shutil.copy(filepath, file_destination)
        else:
            copystatic(filepath, file_destination)




