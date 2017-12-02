Hacarus Backend API V2
=====

Introduction
-----
Backend API for the v2 of mobile app. Utilizes flask as base framework.

#### Running the app

**Dependencies**

- Runs on Python 3.5+
- Install Python3 and pip3 [--Download Page--](https://www.python.org/downloads/)
- MySQL 5.6

**Environment**

- Install virtual env `pip3.5 install virtualenv`
- Run a separate virtual env instance `python3.5 -m venv <env_name>`
- Run the environment `source <evn_name>/bin/activate`

**Install requirements**

- Core dependencies `python3.5 setup.py install`
- Version specific dependencies `pip3.5 install -r requirements.lock`

**Setup database**

To set up database, run the following SQLs one by one

    mysql < data/create_database.sql
    mysql hacarus_v2 < data/create_tables.sql    
    mysql hacarus_v2 < data/create_views.sql
    mysql hacarus_v2 < data/food_data.sql
    mysql hacarus_v2 < data/exercise_data.sql
    mysql hacarus_v2 < data/seed.sql

or just run init_db.sh under `data` directory like this

    cd data
    ./init_db.sh

Be aware that data/create_database.sql will drop and recreate hacarus_v2 database.

**Setup your AWS Credentials**

- Run the following command 
    - `sudo chmod 500 set_aws_creds.sh`
    - `source set_aws_creds.sh`
- Enter your AWS Credentials to set the environment variable


**Running the application**

- Run the application via `python3.5 run.py`
- The default port is 3000. You can access this via `http://localhost:3000/`
- For more options, run `python3.5 run.py --help`

#### Project Structure
```
    +-- app/
    |   +-- api/
    |   |   +-- module/
    |   |   |   +-- __init__.py
    |   |   |   +-- dispatch.py
    |   |   |   +-- model.py
    |   +-- conf/
    |   |   +-- env/
    |   |   |   +-- __init__.py
    |   |   |   +-- development.py
    |   |   |   +-- staging.py
    |   |   |   +-- production.py
    |   |   +-- __init__.py
    |   |   +-- config.py
    |   |   +-- constants.py
    |   +-- lib/
    |   |   +-- __init__.py
    |   |   +-- database.py
    |   |   +-- decorators.py
    |   |   +-- error_handler.py
    |   |   +-- response.py
    |   +-- util/
    |   |   +-- __init__.py
    |   |   +-- utils.py
    |   +-- www/
    |   |   +-- assets/
    |   |   +-- pages/
    |   +-- app.py
    |   +-- __init__.py
    +-- data/
    |   +-- create_database.sql
    |   +-- create_tables.sql
    |   +-- create_views.sql
    |   +-- exercise_data.sql
    |   +-- food_data.sql                
    |   +-- seed.sql
    +-- tests/
    |   +-- start_test.py
    |   +-- module_1_test
    |   |   +-- __init__.py
    |   |   +-- tests.py
    +-- README.md
    +-- requirements.txt
    +-- run.py
    +-- setup.py
```


#### Implementing a module
```
    +-- module/
    |   +-- __init__.py
    |   +-- dispatch.py
    |   +-- model.py
```
###### dispatch
Dispatch is where you store all the request related context. The following are handled by `dispatch.py`
- reuqest handling
- response handling
- routing of request
- authentication

We need to make sure that the request context does not mix with any of the app logic.

###### model
Model is the the one that handles the transactional operations.
- Insert
- Update
- Get
- Search
- Delete

#### Loading custom configuration
The application is accepting custom configuration files in json format.
You need to include these properties as these are required by some of the core libraries in the application.
- APP
- LOGGING
- AWS

For full reference, refer to this sample config file.
```json
{
    "APP_DB": {
        "host": "localhost",
        "db": "hacarus_v2",
        "user": "root",
        "password": "useruser",
        "port": 3306
    },

    "AWS": {
        "COGNITO": {
            "USER_POOL_ID": "ap-northeast-1_ZwU9SnyEL",
            "APP_CLIENT_ID": "792505cfu3gbjfo462en9s1uth",
            "AWS_REGION": "ap-northeast-1",
            "SERVICE_NAME": "cognito-idp"
        },
        "S3": {},
        "EC2": {}
    },

    "LOGGING": {
        "LEVEL": "DEBUG",
        "FORMAT": "[%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s"
    }
}
```

To load the config, just run the application with the `--config` flag.
`python run.py --config <path to config.json>`


#### Tests
The app supports testing using `Flask-Testing` and python's `unittest`. When creating a test for a certain module you need to do the following steps:
- Create a python package folder for the module
    - It should contain 2 files mainly `__init__.py` and `tests.py`
- In `tests.py`, you can add testing for both unit and API testing.
    - Create a class named `APITest` for all the api test cases
    - Create a class named `UnitTest` for all the api test cases
- For more reference on how to create a test case, refer to: [Flask-Testing](https://pythonhosted.org/Flask-Testing/)

###### Running the test cases
You have two options when running the test case, you can either
- Run the all the test cases as a whole using `python -m tests.start_test`
- Run individual tests per module by using `python -m unittest -v tests/<module>/tests.py`

![Running tests with success results](/readme_files/test_case_ok.png?raw=true)


Contributing
-----
Push all the changes to your own branch before making a pull request to the development branch

We use issues in github so make sure that you link the issue to your branch

- Title should be `issue/<issue_number>/title_of_issue`
- Description should have the ff template
```
    ### Summary
        - description of what changed
        - some other details
    ### Tests / Verification / Checklist
        - [ ] List of tests done preferably with screenshots
        - [ ] List of other notes and reminders that needs to be completed
```

**NOTE**
Use the `label` feature of github to indicate tags for the PR.
You can use tags such as:
- `needs code review` if you want others to review your code
- `don't merge yet` if there are still things that needs to be done in the PR
- `task` to indicate that its a task for a milestone


#### API independent dependencies
Some modules are not really needed to run the API. 
- PyPDF2
- hdb (hacarus db implementation)
- textract (swig dependency problems)
- mojimoji

These dependencies will be removed in the future. You can also opt to remove these dependencies in your local requirements.lock if you encounter any problem with them
