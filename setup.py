from setuptools import setup, find_packages

from togglcmder.version import __version__

with open("README.md", "r") as readme:
    long_description = readme.read()

with open("requirements.txt", "r") as requirements:
    required_packages = requirements.read()

setup(
    name='togglcmder',
    version=__version__,
    url="https://github.com/yatesjr/toggl-cmder",
    author="Jonathan Yates",
    author_email="yatesjr@avernakis.com",
    description="Utility to control Toggl timers via the REST API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    install_requires=required_packages.split(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    entry_points={
      'console_scripts': [
          'togglcmder = togglcmder.__main__:main'
      ]
    },
    python_requires='>=3.6'
)
