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
3. [How to run this project](#run-project)\
3.1. [Manual](#manual)\
3.2. [Using docker](#docker)
4. [Run test case](#run-test)
5. [Contact](#contact)

> ## Members :relaxed:: <a name="members"></a>

- [Trần Chí Mỹ - 20110202](https://github.com/mytranchi)
- [Đỗ Dương Thái Tuấn - 20110743](https://github.com/tuanhcmute)

> ## Overview <a name="overview"></a>

1. **Technology**

- [Python 3.9](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [PostgresQL](https://www.postgresql.org/docs/)
- [ORM (Object relational mapping](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- [Jquery](https://jquery.com/)

2. **Structure project**

```
└── Nhom1_CCPTPM/
   ├── .circleci/
   │   └── config.yml
   ├── .github/
   │   └── FUNDING.yml
   ├── app/
   │   ├── authen/
   │   │   ├── __init__.py
   │   │   └── routes.py
   │   ├── main/
   │   │   ├── __init__.py
   │   │   └── routes.py
   │   ├── model/
   │   │   └── user.py
   │   ├── static/
   │   │   ├── css
   │   │   ├── fonts
   │   │   ├── image
   │   │   ├── js
   │   │   └── vendor
   │   ├── templates/
   │   │   ├── base.html
   │   │   ├── data.html
   │   │   ├── index.html
   │   │   ├── login.html
   │   │   └── partials/
   │   │       ├── footer.html
   │   │       ├── header.html
   │   │       └── sidebar-nav.html
   │   ├── utils/
   │   │   └── contants.py
   │   ├── vendor/
   │   │   ├── getToken.py
   │   │   └── getData.py
   │   ├── __init__.py
   │   ├── app
   │   ├── config.py
   │   └── extensions.py
   ├── test/
   │   ├── __init__.py
   │   ├── conftest.py
   │   ├── auth/
   │   │   └── test_login.py
   │   └── main/
   │       └── test_main.py
   ├── .env
   ├── .gitignore
   ├── README.md
   └── requirements.txt
```

> ## How to run this project <a name="run-project"></a>
### Manual <a name="manual"></a>
>
1. [Install python 3.9 (If you don't have)](https://www.python.org/downloads/)

2. Clone project
```
git clone https://github.com/tuanhcmute/Nhom1_CCPTPM
```

3. Run commands:\

**Notice: Please run commands in git bash or other terminal support Linux environment**\

3.1. Create virtual env

```
virtualenv ./venv
```

3.2. Active virtualenv

```
source ./venv/Scripts/activate
```

3.3. Install packakge from pip

```
pip install -r requirements.txt
```

3.4. Load all config from .env file

```
source.env
```

3.5. [Download postgresQL](https://www.postgresql.org/download/) and config username password in postgresQL

3.6. Open `.env` file in this project and change `DATABASE_URI=postgresql://<your_usernamw>:<your_password>@<your_host>:<your_port>/<your_database>"`

3.7. Run project with command. Sever running on http://localhost:50000

```
flask run
```

### Setup project with docker <a name="docker"></a>
1. Clone project
```
git clone https://github.com/tuanhcmute/Nhom1_CCPTPM
```
2. Run docker-compose file
```
docker-compose -f ./docker-compose.yml up -d --build
```
3. If remove container
```
docker-compose -f docker-compose.yml down -v
```


> ## Run test case <a name="run-test"></a>
>
1. Windows

```
pytest
```

2. Linux

```
python -m pytest
```

3.10. Create requirements.txt

```
pip freeze > requirements.txt
```

> ## Contact us <a name="contact"></a>
>
> If you have any question, please contact us through email:

```js
20110743@student.hcmute.edu.vn
```

or

```js
20110202@student.hcmute.edu.vn
```

### Thanks for watching :relaxed::relaxed::relaxed::relaxed:
