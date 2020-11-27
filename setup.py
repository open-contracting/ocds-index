from setuptools import find_packages, setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="ocdsindex",
    version="0.0.2",
    author="Open Contracting Partnership",
    author_email="data@open-contracting.org",
    url="https://github.com/open-contracting/ocds-index",
    description="A command-line tool and library to index OCDS documentation in Elasticsearch",
    license="BSD",
    packages=find_packages(exclude=["tests", "tests.*"]),
    long_description=long_description,
    install_requires=[
        "click",
        "elasticsearch>=7,<8",
        "lxml",
    ],
    extras_require={
        "test": [
            "black==20.8b1",
            "coveralls",
            "pytest",
            "pytest-cov",
        ],
        "docs": [
            "Sphinx",
            "sphinx-autobuild",
            "sphinx_rtd_theme",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "ocdsindex = ocdsindex.cli.__main__:main",
        ],
    },
)
