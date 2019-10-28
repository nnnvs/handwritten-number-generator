from digits_sequence_generator.data_handler import download_mnist
from digits_sequence_generator.data_handler import pre_processing
import numpy as np
import os
from digits_sequence_generator.generator.util import Util


def test_confirm_downloaded_files():
    downloader = download_mnist.DownloadMnist()
    downloader.download_mnist()

    utility = Util()
    config = utility.read_config()
    compressed_folder_path = utility.get_path("mnist_compressed_data_path")
    raw_folder_path = utility.get_path("mnist_raw_data_path")

    for resource in config["mnist_files"]:
        compressed_file_path = os.path.join(compressed_folder_path, resource)
        raw_file_path = os.path.splitext(os.path.join(raw_folder_path, resource))[0]
        assert os.path.exists(compressed_file_path)
        assert os.path.exists(raw_file_path)


def test_mnist_size():
    downloader = download_mnist.DownloadMnist()
    downloader.download_mnist()
    pre_processor = pre_processing.PreProcessing()
    mnist_features, mnist_labels = pre_processor.idx2numpy()

    assert np.shape(mnist_features) == (70000, 28, 28)
    assert np.shape(mnist_labels) == (70000,)
