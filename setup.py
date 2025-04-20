from setuptools import setup, find_packages

setup(
    name="cursor-auto-free",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "colorama==0.4.6",
        "DrissionPage==4.1.0.9",
        "PyQt6==6.6.1",
        "qdarkstyle==3.2.0",
    ],
) 