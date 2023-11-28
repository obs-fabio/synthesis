from setuptools import find_packages, setup

setup(
    name='labsonar_synthesis',
    packages=find_packages(),
    version='0.1.0',
    description='Labsonar Acoustical Synthesis Library',
    author='Anderson Damacena, Fabio Oliveira',
    license='Creative Commons Legal Code',
    install_requires=[],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==4.4.1'],
    # test_suite='tests',
    package_data={'labsonar_synthesis': ['data/*.csv']},
)