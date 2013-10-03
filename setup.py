from setuptools import setup, find_packages

setup(
    name='matcha',
    version='0.0',
    packages=find_packages(),
    url='https://github.com/hirokiky/matcha',
    license='MIT',
    author='hirokiky',
    author_email='hirokiky@gmail.com',
    description='A WSGI dispatcher.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
)
