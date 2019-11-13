from handwritten_number_generator import api_controller
from handwritten_number_generator import generator
import numpy as np

def test_api_generated_image_dimensions():
    app = api_controller.app
    client = app.test_client()
    url = '/generate'

    mock_request_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    mock_request_data = {
        "augment": "true",
        "number": 1234567890,
        "spacing_min": 5,
        "spacing_max": 10,
        "image_width": 300
    }

    response = client.post(url, json=mock_request_data, headers=mock_request_headers)
    generated_image = np.array(response.json["generatedImage"])
    nrows,ncols = np.shape(generated_image)
    assert nrows == 28
    assert ncols == mock_request_data["image_width"]


def test_api_generated_image_normalization():
    """Are the generated image's pixels normalised to values between 0 to 1 ?"""

    app = api_controller.app
    client = app.test_client()
    url = '/generate'
    mock_request_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    mock_request_data = {
        "augment": "true",
        "number": 1234567890,
        "spacing_min": 5,
        "spacing_max": 10,
        "image_width": 300
    }
    response = client.post(url, json=mock_request_data, headers=mock_request_headers)
    generated_image = np.array(response.json["generatedImage"])

    assert np.max(generated_image) <= 1
    assert np.min(generated_image) >= 0


def test_pckg_generated_image_dimensions():
    image_width=56
    generated_image = generator.generate_numbers_sequence(digits=[4,2], spacing_range=(5,10), image_width=image_width)
    nrows,ncols = np.shape(generated_image)
    assert nrows == 28
    assert ncols == image_width


def test_pckg_generated_image_normalization():
    """Are the generated image's pixels normalised to values between 0 to 1 ?"""

    generated_image = generator.generate_numbers_sequence(digits=[4,2], spacing_range=(5,10), image_width=56)
    assert np.max(generated_image) <= 1
    assert np.min(generated_image) >= 0

def test_pckg_generated_image_dtype():
    """The generated image's dtype should be float32"""

    generated_image = generator.generate_numbers_sequence(digits=[4,2], spacing_range=(5,10), image_width=56)
    assert generated_image.dtype == np.dtype('float32')
