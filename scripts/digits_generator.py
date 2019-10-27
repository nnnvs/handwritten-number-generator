import requests
from argparse import ArgumentParser
from PIL import Image
import numpy as np
import time

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def store_image(task_id, processed_image):
    image = Image.fromarray(np.uint8(np.array(processed_image) * 255) , 'L')
    image_name = str(task_id) + ".png"
    image.save(image_name,"PNG")
    print("Image saved successfully as: "+image_name)

parser = ArgumentParser()
parser.add_argument("-n", "--number", type=int, help="Set the number")
parser.add_argument("-a", "--augment", type=int, choices=[0,1], default=0, help="Set the augmentation flag, 1 -> Yes, 0 -> No")
parser.add_argument("-smin", "--spacing_min", type=int, default=5, help="Set minimum value of spacing_range in pixels")
parser.add_argument("-smax", "--spacing_max", type=int, default=10, help="Set maximum value of spacing_range in pixels")
parser.add_argument("-w", "--image_width", type=int, help="Set width of the final image in pixels")

args = parser.parse_args()

url = 'http://127.0.0.1:5000/generate'

if None not in (args.augment, args.number, args.spacing_min, args.spacing_max, args.image_width):
    data = {
        "augment": "true" if args.augment==1 else "false",
        "number": args.number,
        "spacing_min": args.spacing_min,
        "spacing_max": args.spacing_max,
        "image_width": args.image_width
    }
    print("Request data for posting: " + str(data))

    start = time.time()
    post_request = requests.post(url, headers=headers, json=data)

    response_json = post_request.json()
    if(post_request.status_code==200):
        print("Post successful!")
        print("Task Id for your request is " + str(response_json["taskId"]))
        store_image(response_json["taskId"], response_json["generatedImage"])
        print("Process time: " + str(time.time() - start) + " seconds")
    else:
        print("Post Failed!")
        print("Reason: " + str(response_json["status"]))
else:
    print("Arguments not set properly. Please use 'python digits_generator.py -h' for help.")