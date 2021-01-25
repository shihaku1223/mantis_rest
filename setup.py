import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'requests',
]

setuptools.setup(
    name="mantis_rest",
    version="0.0.13",
    author="Shih-Po Wang",
    author_email="shihpo@gmail.com",
    description="The Python binding Mantis REST API",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
