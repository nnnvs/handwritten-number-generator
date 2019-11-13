from handwritten_number_generator.generator.util import Util

def test_read_config():
    utility = Util()
    config = utility.read_config()

    assert len(config.keys()) == 4
    assert config["mnist_compressed_data_path"] == "data/compressed"
    assert config["mnist_raw_data_path"] == "data/raw"
    assert config["processed_image_path"] == "data/processed_images"

def test_create_task_id():
    utility = Util()
    task_id = utility.create_task_id()

    assert len(str(task_id)) == 12