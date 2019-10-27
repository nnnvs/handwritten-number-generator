import logging
import os

import digits_sequence_generator.data_handler.download_mnist as download_mnist
import digits_sequence_generator.data_handler.pre_processing as pre_processing
from digits_sequence_generator.generator import image_generator

mnist_features = []
mnist_labels = []


def init():
    global mnist_features
    global mnist_labels
    downloader = download_mnist.DownloadMnist()
    downloader.download_mnist()
    pre_processor = pre_processing.PreProcessing()
    mnist_features, mnist_labels = pre_processor.idx2numpy()
    logger = logging.getLogger('digits-seq-generator')
    logger.info('starting web-service')


def get_mnist_data():
    return mnist_features, mnist_labels


def set_logger(logging_level=logging.DEBUG):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_folder_path = os.path.join(dir_path,"../")
    logging.basicConfig(filename=os.path.join(config_folder_path,"config/digit-logs.log"),
                        filemode='a',
                        format='[%(asctime)s][%(levelname)s] [%(module)s.py] %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging_level)
    logger = logging.getLogger('digits-seq-generator')
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] [%(module)s.py] %(message)s')
    str_handler = logging.StreamHandler()
    str_handler.setFormatter(formatter)
    str_handler.setLevel(level=logging_level)
    logger.addHandler(str_handler)


"""The function below exists for direct use. Doesn't require task_id. 
Always augments images, if not mentioned otherwise"""
def generate_numbers_sequence(digits, spacing_range, image_width, augment_flag=None):
    if augment_flag is None:
        augment_flag = "true"
    elif augment_flag.lower() == "false":
        augment_flag = "false"
    else:
        augment_flag = "true"

    set_logger(logging.WARNING)
    init()
    digits_str = [str(i) for i in digits]
    number = int("".join(digits_str))
    image_gen = image_generator.ImageGenerator("", augment_flag, number, spacing_range[0], spacing_range[1], image_width)
    return image_gen.generate_digits_sequence()
