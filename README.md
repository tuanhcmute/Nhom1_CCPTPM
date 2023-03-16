# Final Project: API Dashboard

[![My Skills](https://skillicons.dev/icons?i=py,js,jquery,html,css,flask,github,postman,vscode,stackoverflow)](https://skillicons.dev)\

![GitHub labels](https://img.shields.io/github/labels/tuanhcmute/Nhom1_CCPTPM/documentation)
![GitHub repo size](https://img.shields.io/github/repo-size/tuanhcmute/Nhom1_CCPTPM)
![GitHub milestones](https://img.shields.io/github/milestones/open/tuanhcmute/Nhom1_CCPTPM)
![GitHub milestone](https://img.shields.io/github/milestones/issues-open/tuanhcmute/Nhom1_CCPTPM/1)
![GitHub repo file count](https://img.shields.io/github/directory-file-count/tuanhcmute/Nhom1_CCPTPM)

## Table of Contents

1. [Members](#members)
2. [Overview](#overview)
3. [How to run this project](#run-project)
4. [Fourth Example](#fourth-examplehttpwwwfourthexamplecom)

> ## Members :relaxed:: <a name="members"></a>

- [Trần Chí Mỹ - 20110202](https://github.com/mytranchi)
- [Đỗ Dương Thái Tuấn - 20110743](https://github.com/tuanhcmute)

> ## Overview <a name="overview"></a>

1. **Technology**

- [Python 3.9](https://www.python.org/downloads/)

2. Structure project


> ## How to run this project <a name="run-project"></a>

1. [Install python 3.9 (If you don't have)](https://www.python.org/downloads/)
2. Clone project
```js
git clone https://github.com/tuanhcmute/Nhom1_CCPTPM
```
3. Run commands:\
   3.1. Create virtual env

```js
virtualenv ./vnev
```

3.2. Active virtualenv

```js
source ./venv/Scripts/active
```

3.3. Install packakge from pip

```js
pip install -r requirements.txt
```

3.4. Load all config from .env file

```js
source .env;
```

3.5. Run project with command. Sever running on http://localhost:50000

```js
flask run
```

3.6. [Download postgresQL](https://www.postgresql.org/download/) and config username password in postgresQL

3.7. Open `.env` file in this project and change `DATABASE_URI=postgresql://<your_usernamw>:<your_password>@<your_host>:<your_port>/<your_database>"`

3.8. From this project open other terminal run command:

```js
flask shell
```

3.9. Run command create table, create sample data

```js
from extensions import db
from model.user import User
user = User('admin', 'admin')
db.session.add(user)
db.session.commit()
```
