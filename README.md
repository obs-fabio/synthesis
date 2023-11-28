# synthesis
This is an experimental library for the purpose of sonar synthesis based on mathematical modeling

The main idea of ​​this library is to create reusable frameworks to simplify the development, training, visualization and analysis of models and machine learning techniques.

## Installation
To install the synthesis library, in base folder, run the command
```
pip install -e .
```
Besides that, install the machine learning and sonar signal processing libraries, run the commands:
```
git@github.com:obs-fabio/ml.git
cd ml
pip install -e .
cd ..
git@github.com:obs-fabio/sonar.git
cd sonar/python
pip install -e .
cd ../..
```

## Use

This project assumes an execution in a docker available in dockerhub
```
docker pull fabioobs/pytorch
```
