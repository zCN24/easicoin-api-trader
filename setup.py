"""
Easicoin API Python客户端库 - 设置脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="easicoin-api",
    version="1.0.0",
    author="Easicoin Developer",
    author_email="support@easicoin.io",
    description="Easicoin交易所官方Python API客户端库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/easicoin/easicoin-api-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "websocket-client>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.20.0",
            "black>=23.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
    },
)
