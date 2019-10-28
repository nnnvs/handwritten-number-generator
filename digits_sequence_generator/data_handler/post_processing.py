import numpy as np
import random
import os
import logging
from PIL import Image
from digits_sequence_generator.generator.util import Util

logger = logging.getLogger('digits-seq-generator')

utility = Util()
config = utility.read_config()

class PostProcessing:

    def __init__(self, task_id, number, spacing_min, spacing_max, image_width):
        self.task_id = task_id
        self.number = number
        self.spacing_min = spacing_min
        self.spacing_max = spacing_max
        self.image_width = image_width
        self.processed_folder_path = utility.get_path("processed_image_path")


    def find_right_most_non_black_column(self, np_array):
        nrows, ncols = np.shape(np_array) # should be 28x28
        right_most_non_black_col = ncols-1
        for col in range(ncols-1, -1, -1):
            if np.mean(np_array[:,col]) != 0:
                right_most_non_black_col = col
                break
        return right_most_non_black_col

    def find_left_most_non_black_column(self, np_array):
        nrows, ncols = np.shape(np_array)  # should be 28x28
        left_most_non_black_column = 0
        for col in range(0, ncols):
            if np.mean(np_array[:, col]) != 0:
                left_most_non_black_column = col
                break
        return left_most_non_black_column

    def delete_black_space_from_image(self, np_array):
        nrows,ncols = np.shape(np_array)  # should be 28x28
        right_limit = self.find_right_most_non_black_column(np_array)+1
        left_limit = self.find_left_most_non_black_column(np_array)-1

        np_array = np.delete(np_array, np.s_[right_limit:(ncols-1)+1], 1)  # adding +1 to upper limit of np.s_ slice for complete deletion of black area
        np_array = np.delete(np_array, np.s_[0:left_limit+1], 1)
        return np_array

    def create_spacing_array(self, spacing_min, spacing_max):
        random_number = int(random.uniform(spacing_min, spacing_max))
        return np.zeros([28,random_number])

    def stitch_arrays(self, cropped_arrays):
        stitched_array = cropped_arrays[0]
        for index in range(1, len(cropped_arrays)):
            spacing_array = self.create_spacing_array(self.spacing_min, self.spacing_max)
            stitched_array = np.concatenate((stitched_array, spacing_array, cropped_arrays[index]), axis=1)
        return stitched_array

    def add_padding(self, image_normalized):
        spacing_array = np.zeros([28,4])
        image_normalized = np.concatenate((spacing_array, image_normalized, spacing_array), axis=1)
        return image_normalized

    def stretch_image(self, numpy_array):
        image = Image.fromarray(np.uint8(numpy_array * 255), 'L')
        image_resized = image.resize((self.image_width, 28))
        return image_resized

    def normalize_image(self, image):
        image = np.array(image).astype('float32') / 255
        return image

    def store_image(self, processed_image):
        image = Image.fromarray(np.uint8(processed_image * 255) , 'L')
        image.save(self.processed_folder_path + "/" + str(self.task_id) + "_" + str(self.number)[:20] + ".png","PNG")

    def post_processing(self, augmented_images):
        cropped_arrays=[]
        logger.info("[Task Id: " + str(self.task_id) + "]. Begin post processing augmented images...")
        for augmented_image in augmented_images:
            cropped_arrays.append(self.delete_black_space_from_image(augmented_image))
        logger.info("[Task Id: " + str(self.task_id) + "]. Cropping images done.")
        stitched_array = self.stitch_arrays(cropped_arrays)
        logger.info("[Task Id: " + str(self.task_id) + "]. Stitching images done.")
        padded_stitched_array = self.add_padding(stitched_array)
        logger.info("[Task Id: " + str(self.task_id) + "]. padding images done.")
        image_resized = self.stretch_image(padded_stitched_array)
        logger.info("[Task Id: " + str(self.task_id) + "]. resizing images done.")
        image_normalized = self.normalize_image(image_resized)
        self.store_image(image_normalized)

        return image_normalized.astype('float32')

