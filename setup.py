import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
  name="easyjsonparser",
  version="1.1.1",
  author="Avi SZYCHTER",
  author_email="xentsc2@gmail.com",
  description="Serialize and deserialize JSON documents to Python data structures",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/xatavian/easyjsonparser",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ]
)
