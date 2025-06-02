from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="asl-recognition",
    version="1.0.0",
    author="Pratham",
    description="Real-time American Sign Language Recognition System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pratham/asl-recognition",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "asl-train=Scripts.train.train:main",
            "asl-test=Scripts.train.test_live:main",
            "asl-server=server.App:main",
        ],
    },
)