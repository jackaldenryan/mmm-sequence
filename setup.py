from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mmm-sequence",
    version="0.1.0",
    author="Jack Ryan",
    author_email="jackaldenryan@gmail.com",
    description="A package for generating and analyzing max-minus-min sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackaldenryan/mmm-sequence",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.9",
    install_requires=[
        "numpy",
        "matplotlib",
        "graphviz",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "mmm-sequence=mmm_sequence.cli:cli",
        ],
    },
)
