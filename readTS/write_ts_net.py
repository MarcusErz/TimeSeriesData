from definition import TARGET_DIR
import numpy as np
import os


def networks_to_file(sparsifyed_networks, source_filename):
    name, ending = source_filename.split('.')
    taget_data_path = os.path.join(TARGET_DIR, name)
    for i in range(len(sparsifyed_networks)):
        target_file_name = name + "{:04}".format(i) + '.' + ending
        target_path = os.path.join(taget_data_path, target_file_name)
        f = open(target_path, "w")
        indexes = np.where(sparsifyed_networks[i] != 0)
        assert len(indexes[0] == len(indexes[1]))
        for y in range(len(indexes[0])):
            f.write(str(indexes[0][y]) + " " + str(indexes[1][y]) + "\n")
        f.close()
