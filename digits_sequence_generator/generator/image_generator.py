import logging
from digits_sequence_generator import generator
import numpy as np
import random
from digits_sequence_generator.generator import digits_augmentor
from digits_sequence_generator.data_handler import post_processing

logger = logging.getLogger('digits-seq-generator')


class ImageGenerator:

    def __init__(self, task_id, augment_flag, number, spacing_min, spacing_max, image_width):
        self.task_id = task_id
        self.augment_flag = str(augment_flag)
        self.number = number
        self.spacing_min = spacing_min
        self.spacing_max = spacing_max
        self.image_width = image_width
        self.mnist_features, self.mnist_labels = generator.get_mnist_data()

    """The below function also requires task_id for managing purposes."""
    def generate_digits_sequence(self):
        chosen_images = self.fetch_random_images()
        if self.augment_flag.lower() == "true":
            digit_augmentor = digits_augmentor.DigitsAugmentor(self.task_id)
            augmented_images = digit_augmentor.augment_images(digit_augmentor.augmentation_config(), chosen_images)
        else:
            augmented_images = chosen_images

        post_process = post_processing.PostProcessing(self.task_id, self.number, self.spacing_min, self.spacing_max, self.image_width)
        processed_image = post_process.post_processing(augmented_images)

        return processed_image

    def fetch_random_images(self):
        chosen_images = []
        logger.info("[Task Id: " + str(self.task_id) + "]. Choosing random images for " + str(self.number))
        for number in [int(d) for d in str(self.number)]:
            digit_index_list = np.where(self.mnist_labels == number)[0]
            random_index = random.randint(0, len(digit_index_list)-1)
            chosen_images.append(self.mnist_features[digit_index_list[random_index]])
        return chosen_images
