from setuptools import setup, find_packages

setup(
    name="youtube-audio-extractor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytube==15.0.0",
        "pydub==0.25.1",
        "pytest==7.4.3",
        "pytest-mock==3.12.0"
    ]
) 