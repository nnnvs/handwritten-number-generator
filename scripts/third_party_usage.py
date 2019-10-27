from PIL import Image
import numpy as np
from digits_sequence_generator import generator

# third party usage example. Generates 42

def store_image(processed_image):
    image = Image.fromarray(np.uint8(processed_image * 255) , 'L')
    image_name = "example.png"
    image.save(image_name,"PNG")
    print("Image saved successfully as: "+image_name)

store_image(generator.generate_numbers_sequence([4,2],(5,10),56))