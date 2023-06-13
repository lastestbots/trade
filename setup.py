from setuptools import setup, find_packages

setup(
    name='trade',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests'],
    include_package_data=True,
    author='cyw',
    author_email='2762383426@qq.com',
    description='量化交易工具包',

)
