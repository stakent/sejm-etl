Table of contents
- [Description](#description)
- [ETL for acts](#etl-for-acts)
- [Installation](#installation)
- [Running](#running)
- [Settings](#settings)


# Description

This project contains an ETL pipeline for processing data exposed by the Sejm (Polish parliament) API.
There are two main components of this data:
- Data related to the Sejm's legislative acts
- Data related to the Sejm's members of parliament and Sejm's proceedings

# ETL for acts
ETL stands for: Extract, Transform, Load.
This pipeline is a data integration process that involves three main steps:

- [x] Extract:
    The process of retrieving acts from Sejm's API.
    - [x] The lists of legislative acts are retrieved from the Sejm's for each publication year and publisher.
    - [x] For each legislative act the act text in PDF format as published by the Sejm is retrieved then stored in file cache.

- [x] Transform:
    - [x] For each act the act text is converted from PDF to plain text.
    - [x] The words divisions at the end of the lines are reversed, the page headers are removed.
    - [x] The transformed text is then stored in a file cache.

- [ ] Load:
    - [ ] each act is split into chunks
    - [ ] for each chunk it's vector representation is calulated
    - [ ] the vector representations are then stored in the vector database

# Installation

- clone this repository and change working directory
```shell
https://github.com/stakent/sejm-etl.git
cd sejm-etl
```

- activate recent Python version
```shell
pyenv shell 3.12.11
```

- create and activate virtual environment
```shell
python -m venv venv
```

- install dependencies
```shell
pip install -r requirements/dev.txt
```

# Running
Use provided shell script
```shell
./run-sejm-etl.sh
```

See in the shell script how to override default settings values.


# Settings
| Name                       | Type | Default value | Description                            |
| -------------------------- | ---- | ------------- | -------------------------------------- |
| app_name                   | str  | "sejm-etl"    | Application name                       |
| env                        | str  | "dev"         | Environment type                       |
| log_level                  | int  | logging.INFO  | Logging level                          |
| requests_external_timeout  | int  | 10            | External requests calls timeout        |
| number_of_years_to_process | int  | 3             | How many years of past data to process |
| cache_base_dir_prefix      | str  | "/tmp"        | Location of data cache                 |

