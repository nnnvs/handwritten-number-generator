import logging
import cv2
from albumentations import (
    ShiftScaleRotate, Blur, OpticalDistortion, GridDistortion, ElasticTransform,
    GaussNoise, MedianBlur, RandomBrightnessContrast,
    IAAEmboss, OneOf, Compose
)

logger = logging.getLogger('digits-seq-generator')

class DigitsAugmentor:

    logger = logging.getLogger('digits-seq-generator')

    def __init__(self,task_id):
        self.task_id = task_id

    def augmentation_config(self,p=0.5):
        return Compose([
            GaussNoise(var_limit=(0.0, 0.005),p=0.1),
            OneOf([
                # MotionBlur(blur_limit=3,p=0.1), #works in a weird way
                MedianBlur(blur_limit=3,p=0.1),
                Blur(blur_limit=3,p=0.2)
            ], p=0.2),
            ShiftScaleRotate(shift_limit=0.1,scale_limit=0.4, border_mode=cv2.BORDER_CONSTANT,p=0.2),
            OneOf([
                GridDistortion(num_steps=3, distort_limit=0.3, border_mode=cv2.BORDER_CONSTANT,p=0.1),
                ElasticTransform(sigma=200,alpha_affine=5,border_mode=cv2.BORDER_CONSTANT,p=0.2),
                OpticalDistortion(distort_limit=0.1, shift_limit=0.1,border_mode=cv2.BORDER_CONSTANT,p=0.2)
            ], p=0.2),
            OneOf([
                # IAASharpen(alpha=(0.01, 0.05), lightness=(0.01, 0.05)),
                IAAEmboss(alpha=(0.01, 0.05),strength=(0.1, 0.4)),
                RandomBrightnessContrast(brightness_limit=0.4, contrast_limit=0.4,p=0.2)
            ], p=0.2)
        ], p=p)

    def augment_images(self, augmentation,images):
        logger.info("[Task Id: " + str(self.task_id) + "]. Begin augmenting images...")
        augmented_images = []
        for image in images:
            augmented_images.append(augmentation(image=image)['image'])
        return augmented_images
