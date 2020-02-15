from setuptools import setup, find_packages

setup(
    name="ay",
    version="0.1",
    author="Ruben Afonso",
    author_email="rbfrancos@gmail.com",
    description="Tiny framework for generative art using Python",
    url="https://github.com/rubenafo/ay",
    keywords = ["generative art", "cairo", "generative", "python", "design"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
