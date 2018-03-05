from setuptools import setup, find_packages
setup(
    name='burnlight',
    version='0.1.0',
    description='GPIO scheduler for Raspberry Pis',
    author='Matthew Casserly',
    author_email='',
    url='https://github.com/wailashi/burnlight',
    license=license,
    packages=find_packages(exclude=('tests'))
)
