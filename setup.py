from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    README = fh.read()

setup(
    name='burnlight',
    version='0.2.0',
    description='GPIO scheduler for Raspberry Pis',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Matthew Casserly',
    author_email='',
    entry_points={
        'console_scripts': [
            'burnlight = burnlight.client.client:cli',
            'burnlightd = burnlight.server.server:main',
        ]
    },
    install_requires = [
        'flask>=1.0.0',
        'lark-parser',
        'gevent',
        'click',
        'gpiozero',
        'requests'

    ],
    url='https://github.com/wailashi/burnlight',
    license='MIT',
    packages=find_packages(exclude=('tests')),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
