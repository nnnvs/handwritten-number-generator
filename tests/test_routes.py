from handwritten_number_generator import api_controller


def test_health():
    app = api_controller.app
    client = app.test_client()
    url = '/health'

    response = client.get(url)
    assert response.json["Status"] == "Running"
    assert response.status_code == 200


def test_post_success_with_augment():
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
    assert response.status_code == 200

def test_post_success_without_augment():
    app = api_controller.app
    client = app.test_client()
    url = '/generate'

    mock_request_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    mock_request_data = {
        "augment": "false",
        "number": 1234567890,
        "spacing_min": 5,
        "spacing_max": 10,
        "image_width": 300
    }

    response = client.post(url, json=mock_request_data, headers=mock_request_headers)
    assert response.status_code == 200


def test_post_failure_unauthorized_header():
    app = api_controller.app
    client = app.test_client()
    url = '/generate'

    mock_request_headers = {
        'Content-Type': 'text/plain',
    }

    mock_request_data = {
        "augment": "true",
        "number": 1234567890,
        "spacing_min": 5,
        "spacing_max": 10,
        "image_width": 300
    }

    response = client.post(url, json=mock_request_data, headers=mock_request_headers)
    print(response.json)
    assert response.status_code == 400
    assert b"Request content type should be application/json." == response.get_data()


def test_post_failure_bad_request():
    app = api_controller.app
    client = app.test_client()
    url = '/generate'
    mock_request_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    mock_request_data = {}
    response = client.post(url, json=mock_request_data, headers=mock_request_headers)
    assert response.status_code == 400
    assert response.json["status"] == "Request JSON incomplete"


def test_post_failure_incompatible_type():
    app = api_controller.app
    client = app.test_client()
    url = '/generate'
    mock_request_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    mock_request_data = {
        "augment": "true",
        "number": 1234,
        "spacing_min": 5,
        "spacing_max": 10,
        "image_width": "300"
    }
    response = client.post(url, json=mock_request_data, headers=mock_request_headers)
    assert response.status_code == 500


def test_post_failure_null_check():
    app = api_controller.app
    client = app.test_client()
    url = '/generate'
    mock_request_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    mock_request_data = {
        "augment": "true",
        "number": 1234,
        "spacing_min": 5,
        "spacing_max": 10,
        "image_width": None
    }
    response = client.post(url, json=mock_request_data, headers=mock_request_headers)
    assert response.status_code == 400
    assert response.json["status"] == "Empty feature(s)"
