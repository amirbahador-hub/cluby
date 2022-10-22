# cluby
https://cluby.com/ assessment

## Setup

create .env file in config/.env
```bash
touch config/.env
```

setup some keys in env 
if you are using exsisting database setup DB_MANAGED = False or Nothing
but if you are creeting your database DB_MANAGED = True
```
DB_HOST=database host
DB_PORT=port database
DB_USER=user database
DB_PASS=database password
DB_NAME=database name
DB_MANAGED=False 
```

if your DB_MANAGED=True
```bash
python manage.py makemigrations
python manage.py migrate
```

install requirements
```
pip install requirements.txt
```

## RUN IN DEVELOPMENT MODE
Add ENV_NAME KEY to config/.env
```
ENV_NAME=dev
```
install dev requirements
```
pip install requirements_dev.txt
```


runserver
```bash
python manage.py runserver
```

## RUN TESTS
```bash
pytest . -rP
```

## Add dependencies

### Main requirements
add your dependency to requirements.in
```
pip-compile requirements.in --output-file=requirements.txt
```

### Development requirements
add your dependency to requirements_dev.in
```
pip-compile requirements_dev.in --output-file=requirements_dev.txt
```
