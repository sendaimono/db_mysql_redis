# ADB project - Movie Rental

This is python **chalice** project using **MySQL** and **Redis** Cache

## Current features

List of features **Movie Rental** provides:

* docker-compose.yml file to create env

### Register user (/register) POST

**Request body**:
```json
{
	"login": "aaa",
	"password": "password",
	"username": "Mikolaj"
}
```
**Response**:
```json
{
	"ok": true|false
}
```
### Login user (/login) POST
**Request body**:
```json
{
	"login": "aaa",
	"password": "password"
}
```
**Response**:
```json
{
    "ok": true,
    "data": {
        "username": "sendaimono",
        "token": "KZNdbSZLVSFQBmhBcsblgZmV7aS65jU994873HrH8Ff46WcX7V2WkOc2YxWEo6vr"
    }
}
```
### Create movie(/create-movie) POST
**Request headers**:
```json
{
    "content-type": "application/json",
    "Authorization": "KZNdbSZLVSFQBmhBcsblgZmV7aS65jU994873HrH8Ff46WcX7V2WkOc2YxWEo6vr"
}
```
**Request body**:
```json
{
	"name": "Some new movie",
	"description": "ahsdjfhjaksh kdhfjahsdjhfajsdlfl asldhf",
	"premiere_date": "2019-01-15T12:14:20.488Z"
}
```
**Response**:
```json
{
    "ok": true
}
```
### Get movie(/get-movie?gid=<movie_gid>) GET
**Request headers**:
```json
{
    "content-type": "application/json",
    "Authorization": "KZNdbSZLVSFQBmhBcsblgZmV7aS65jU994873HrH8Ff46WcX7V2WkOc2YxWEo6vr"
}
```
**Response**:
```json
{
    "ok": true,
    "data": {
        "gid": "E5a7Ywyt",
        "name": "Some new movie",
        "description": "ahsdjfhjaksh kdhfjahsdjhfajsdlfl asldhf lahsdj fhasjdk fhajskhdf jkahsdjf asldjh fajslhdjfhalsdjhfjasdh fljahsdjfh  asjhdfjahs dlfhajs dfajhs djhaf dshfjlhasd hfljash dfjahsdfahsjdhf ajshd fasjdfh lashdf",
        "premiere_date": "2019-01-15T12:14:20.488000"
    }
}
```
### List movies(/list-movies) GET
**Request headers**:
```json
{
    "content-type": "application/json",
    "Authorization": "KZNdbSZLVSFQBmhBcsblgZmV7aS65jU994873HrH8Ff46WcX7V2WkOc2YxWEo6vr"
}
```
**Response**:
```json
{
    "ok": true,
    "data": [
        {
            "gid": "E5a7Ywyt",
            "name": "Some new movie",
            "short_desc": "ahsdjfhjaksh kdhfjahsdjhfajsdlfl asldhf lahsdj fha..."
        }
    ]
}
```
### Create review(/create-review) POST
**Request headers**:
```json
{
    "content-type": "application/json",
    "Authorization": "KZNdbSZLVSFQBmhBcsblgZmV7aS65jU994873HrH8Ff46WcX7V2WkOc2YxWEo6vr"
}
```
**Request body**:
```json
{
	"content": "ahsdfjkhasdfjahsdjhfjahsdja df asdh jfahsdf jhasdfhasdhf",
	"mark": 10,
	"movie_gid": "E5a7Ywyt"
}
```
**Response**:
```json
{
    "ok": true
}
```
### Get reviews(/get-reviews?gid=<movie_gid>) GET
**Request headers**:
```json
{
    "content-type": "application/json",
    "Authorization": "KZNdbSZLVSFQBmhBcsblgZmV7aS65jU994873HrH8Ff46WcX7V2WkOc2YxWEo6vr"
}
```
**Response**:
```json
{
    "ok": true,
    "data": [
        {
            "author": "sendaimono",
            "created": "2019-01-15T17:49:12.579474",
            "mark": 10,
            "content": "ahsdfjkhasdfjahsdjhfjahsdja df asdh jfahsdf jhasdfhasdhf asdhf ajsdhf asdflahds hajsdh fahsdf jahsd fajhsdf jhsd jafhsdl haflhsd asdfasd1"
        }
    ]
}
```
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

### Run migration script for PostgreSQL

Install PosgreSQL server locally, set username to `postgres`(default) and password to `root` and create db `chat` inside it.

Go to folder repo folder and run
```sh
(venv)$ cd db_schema
(venv)$ alembic upgrade head
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