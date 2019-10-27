from flask import Flask, jsonify
from flask import request
from digits_sequence_generator import generator
from digits_sequence_generator.generator.image_generator import ImageGenerator
from digits_sequence_generator.generator.util import Util
import traceback
import logging

app = Flask(__name__)


def initialize_app():
    generator.set_logger()
    generator.init()


initialize_app()
utility = Util()


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'Status': 'Running'})


@app.route('/generate', methods=['POST', 'PUT'])
def generate():
    logger = logging.getLogger('digits-seq-generator')
    if request.headers['Content-Type'] == 'application/json':
        task_id = None
        try:
            task_id = utility.create_task_id()
            augment_flag = request.json["augment"]
            number = request.json["number"]
            spacing_min = request.json["spacing_min"]
            spacing_max = request.json["spacing_max"]
            image_width = request.json["image_width"]

            if None not in (task_id, number, spacing_min, spacing_max, image_width):
                logger.info('[Task Id: ' + str(task_id) + ']. Generation request data: ' + str(request.json))
                image_gen = ImageGenerator(task_id, augment_flag, number, spacing_min, spacing_max, image_width)
                request.json["generatedImage"] = image_gen.generate_digits_sequence().tolist()
                request.json["taskId"] = task_id
                logger.info('[Task Id: ' + str(task_id) + ']. Generation request completed.')
                return jsonify(request.json)
            else:
                logger.info('[Task Id: ' + str(task_id) + ']. Generation request received for empty features')
                response = jsonify({'TaskId': task_id, 'requestBody': request.json, 'status': 'Empty feature(s)'})
                return response, 400

        except Exception:
            stack_trace = traceback.format_exc()
            logger.info('[Task Id: ' + str(task_id) + ']. Digit Augmentor Failed. \n'+stack_trace)
            response = jsonify({'TaskId': task_id, 'requestBody': request.json, 'status': stack_trace})
            return response, 500
    else:
        return "Request content type should be application/json.", 400


# Added for local testing
if __name__ == "__main__":
    app.run()
