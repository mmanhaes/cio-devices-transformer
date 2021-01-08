import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="devices_transformer_marcelo", # Replace with your own username
    version="0.0.1",
    author="Marcelo Mota Manhaes",
    author_email="mmanhaes@br.ibm.com",
    description="This package will transform devices input data to estimators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.ibm.com/CIO-Insights-Lab/cio-devices-transformer.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
