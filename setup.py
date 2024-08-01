from os import path
from setuptools import setup, find_packages

main_dir = path.abspath(path.dirname(__file__))
packages = find_packages(exclude=["*.tests", "*.tests.*", "test*", "tests"])
packages.append("config")

setup(
    name='resecrets',
    version='0.1',
    packages=packages,
    install_requires=[],  # requirements.txt
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'resecrets=resecrets.main:main',
        ],
    },
    author='Walleson Rodrigues',
    author_email='phorensic@pm.me',
    description='Description of resecrets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/phor3nsic/resecrets',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
