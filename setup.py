from setuptools import find_packages
from setuptools import setup

setup(
    name="dag_gettsim",
    version="0.0.1",
    description="Explore the use of DAGs in gettsim.",
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 2 - Pre-Alpha",
    ],
    url="https://github.com/janosg/dag_gettsim",
    author="Janos Gabler",
    author_email="janos.gabler@gmail.com",
    packages=find_packages(),
    zip_safe=False,
)
