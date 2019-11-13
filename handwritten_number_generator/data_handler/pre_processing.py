import struct as st
import numpy as np
import os, logging
from handwritten_number_generator.generator.util import Util

logger = logging.getLogger('digits-seq-generator')

class PreProcessing:

    def __init__(self):
        utility = Util()
        self.config = utility.read_config()
        self.raw_folder_path = utility.get_path("mnist_raw_data_path")


    def read_idx(self, file_path):
        with open(file_path, 'rb') as file:
            zero, data_type, dims = st.unpack('>HBB', file.read(4))
            shape = tuple(st.unpack('>I', file.read(4))[0] for d in range(dims))
            return np.frombuffer(file.read(), dtype=np.uint8).reshape(shape)

    def normalize_mnist(self, mnist):
        mnist = mnist.astype('float32') / 255
        return mnist

    def idx2numpy(self):
        mnist=[]
        logger.info("Converting Mnist idx files to numpy arrays")
        for resource in self.config["mnist_files"]:
            np_array = self.read_idx(os.path.splitext(os.path.join(self.raw_folder_path, resource))[0])
            mnist.append(np_array)
        mnist_features = np.concatenate((mnist[0], mnist[2]),axis = 0)
        labels = np.concatenate((mnist[1], mnist[3]),axis = 0)
        mnist_features = self.normalize_mnist(mnist_features)
        return mnist_features, labels
