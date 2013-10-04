import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='matcha',
    version='0.0',
    #packages=find_packages(),
    py_modules=['matcha'],
    url='https://github.com/hirokiky/matcha',
    license='MIT',
    author='hirokiky',
    author_email='hirokiky@gmail.com',
    description='A WSGI dispatcher.',
    long_description=README,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
    tests_require=['pytest'],
)
