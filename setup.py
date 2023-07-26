from setuptools import setup
from src._version import __version__

setup(
    name='ffmpeg-py',
    version=__version__,
    author='Gautam Dhingra',
    author_email="gautamdhingra8404@gmail.com",
    download_url='http://pypi.python.org/pypi/ffmpeg-py',
    description='Simple Python wrapper for FFmpeg',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    project_urls={
        "Source": "https://github.com/gautam8404/ffmpeg-py"
    },
    python_requires='>=3.5'
)