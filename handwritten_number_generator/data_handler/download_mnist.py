from __future__ import division
from __future__ import print_function

import gzip
import logging
import os
import sys
import traceback
from urllib.error import URLError
from urllib.request import urlretrieve

from handwritten_number_generator.generator.util import Util

logger = logging.getLogger('digits-seq-generator')


class DownloadMnist:

    def __init__(self):
        utility = Util()
        self.config = utility.read_config()
        self.compressed_folder_path = utility.get_path("mnist_compressed_data_path")
        self.raw_folder_path = utility.get_path("mnist_raw_data_path")

    @staticmethod
    def show_download_progress(chunk_number, chunk_size, file_size):
        if file_size != -1:
            percent = min(1, (chunk_number * chunk_size) / file_size)
            bar = '#' * int(64 * percent)
            sys.stdout.write('\r0% |{:<64}| {}%'.format(bar, int(percent * 100)))

    def download_mnist_zip(self, resource):
        url = 'http://yann.lecun.com/exdb/mnist/{}'.format(resource)
        compressed_file_path = os.path.join(self.compressed_folder_path, resource)
        if os.path.exists(compressed_file_path):
            logger.info('File {} already exists, skipping ...'.format(compressed_file_path))
        else:
            logger.info('Downloading {} ...'.format(url))
            try:
                hook = self.show_download_progress
                urlretrieve(url, compressed_file_path, reporthook=hook)
            except URLError:
                raise RuntimeError('Error downloading resource!')

    def unzip_mnist(self, resource):
        compressed_file_path = os.path.join(self.compressed_folder_path, resource)
        raw_file_path = os.path.splitext(os.path.join(self.raw_folder_path, resource))[0]
        if os.path.exists(raw_file_path):
            logger.info('File {} already exists, skipping ... '.format(raw_file_path))
            return
        with gzip.open(compressed_file_path, 'rb') as compressed_file:
            with open(raw_file_path, 'wb') as raw_file:
                raw_file.write(compressed_file.read())
                logger.info('Unzipped {} ...'.format(compressed_file_path))

    def download_mnist(self):
        try:
            logger.info("Begin downloading MNIST data...")
            for resource in self.config["mnist_files"]:
                self.download_mnist_zip(resource)
                self.unzip_mnist(resource)
            logger.info("Downloaded MNIST data successfully")
        except Exception:
            logger.warning(traceback.format_exc())
            exit(42)
