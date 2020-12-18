# Website-Project

## Installation

clone:
```
$ git clone https://github.com/Ted-0711/Website_Project.git
$ cd Website_Project
```
create & activate virtual env then install dependency:

with venv/virtualenv + pip:
```
$ python -m venv env  # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ pip install -r requirements.txt
```
or with Pipenv:
```
$ pipenv install --dev
$ pipenv shell
```
init database then run:
```
$ flask initdb
$ flask run
* Running on http://127.0.0.1:5000/
```
