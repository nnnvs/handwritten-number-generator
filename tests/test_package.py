from digits_sequence_generator import generator
import pytest

def test_generator_empty_variables():
    with pytest.raises(ValueError):
        generated_image = generator.generate_numbers_sequence(digits=[], spacing_range=(), image_width=None)


def test_generator_incompatible_type():
    with pytest.raises(TypeError):
        generated_image = generator.generate_numbers_sequence(digits=["3","4","4"], spacing_range=("1","2"), image_width="54")


def test_generator_null_check():
    with pytest.raises(ValueError):
        generated_image = generator.generate_numbers_sequence(digits=None, spacing_range=None, image_width=None)

def test_generator_negative_numbers():
    with pytest.raises(ValueError):
        generated_image = generator.generate_numbers_sequence(digits=[4,-2], spacing_range=(5,-10), image_width=-56)
