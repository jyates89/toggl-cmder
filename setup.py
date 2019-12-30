from setuptools import setup, find_packages

from togglcmder.version import __version__

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name='togglcmder',
    version=__version__,
    url="https://github.com/yatesjr/toggl-cmder",
    author="Jonathan Yates",
    author_email="yatesjr@avernakis.com",
    description="Utility to control Toggl timers via the REST API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    entry_points={
      'console_scripts': [
          'toggle_cmder = togglcmder.main:main'
      ]
    },
    python_requires='>=3.6'
)
