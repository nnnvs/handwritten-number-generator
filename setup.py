from setuptools import find_packages, setup

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='digits_sequence_generator',
      version='1.0.0',
      description='Generates images of the sequentially stacked augmented digits from MNIST data for training purposes.',
      long_description=readme(),
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Image Augmentation',
      ],
      author='Nikhil Vinay Sharma',
      author_email='nikhilvs999@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      )
