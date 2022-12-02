from setuptools import find_packages, setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="ocdsindex",
    version="0.1.0",
    author="Open Contracting Partnership",
    author_email="data@open-contracting.org",
    url="https://github.com/open-contracting/ocds-index",
    description="A command-line tool and library to index OCDS documentation in Elasticsearch",
    license="BSD",
    packages=find_packages(exclude=["tests", "tests.*"]),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=[
        "click",
        "elasticsearch>=7,<8",
        "lxml",
    ],
    extras_require={
        "test": [
            "coveralls",
            "pytest",
            "pytest-cov",
        ],
        "docs": [
            "furo",
            "sphinx",
            "sphinx-autobuild",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={
        "console_scripts": [
            "ocdsindex = ocdsindex.__main__:main",
        ],
    },
)
