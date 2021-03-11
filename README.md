# project-template

This is code handling recommendations for the online platform

## Overview

This project template contains code for the RESTful API for the Recommendations (A relationship between two products (prod a goes with prod b).

The `/service` folder contains your `models.py` file for your model and a `service.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. 

## Setup

see Wiki

## Contents

The project contains the following:

```text
.coveragerc         - settings file for code coverage options
.gitignore          - this will ignore vagrant and other metadata files
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/            - service python package
├── __init__.py     - package initializer
├── models.py       - module with business models
└── service.py      - module with service routes

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for busines models
└── test_service.py - test suite for service routes

Vagrantfile         - Sample Vagrant file that installs Python 3 and PostgreSQL
```

This repository is part of the NYU class **CSCI-GA.2810-001: DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Curant Institute, Graduate Division, Computer Science.
