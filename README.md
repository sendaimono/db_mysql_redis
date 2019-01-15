# ADB project - Movie Rental

This is python **chalice** project using **MySQL** and **Redis** Cache

## Current features

List of features **Movie Rental** provides:

* docker-compose.yml file to create env
* empty chalice project

## Start from scratch

You need python 3.6 and pip3.6 installed

### Create virtualenv and open it

Do this inside cloned repo(where `app.py` is located)

```bash
$  python3.6 -m pip install virtualenv
$  virtualenv venv
$  source venv/bin/activate
(venv)$  pip install -r requirements.txt
```

### Setup dockers

Go to folder repo folder and run
```sh
(venv)$ docker-compose up -d
```

### Run server

In folder where `app.py` is located run:
```sh
(venv)$ chalice local
```