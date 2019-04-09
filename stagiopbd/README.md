# API DJANGO

### BEFORE FIRST RUN
```sh
cd 1_Paciente/paciente/paciente

if it runs in docker:
    sudo docker-compose up --build -d
    sudo docker exec -ti paciente bash
    python3 manage.py makemigrations paciente quadro_clinico alergia
    python3 manage.py migrate
else:
    # start mysql
    sudo apt install python3-dev python3-pip
    sudo pip3 install -r requirements.txt
    python3 manage.py makemigrations paciente quadro_clinico alergia
    python3 manage.py migrate
    
```

### TO RUN (after first)
```sh
python3 manage.py runserver
OR
sudo docker-compose up -d
```

### API
```sh
http://127.0.0.1:8000/stagiop_bd/api/paciente
http://127.0.0.1:8000/stagiop_bd/api/alergia
http://127.0.0.1:8000/stagiop_bd/api/quadro_clinico
```

### GUI
```sh
http://127.0.0.1:8000/stagiop_bd
```

### TESTES
```sh
python3 manage.py test paciente
python3 manage.py test alergia
python3 manage.py test quadro_clinico
```

### ENVIRONMENTS
* __DB_USER__ = database user
* __DB_NAME__ = database name
* __DB_PASSWORD__ = database password
* __DB_HOST__ = database host
* __DB_PORT__ = database port
* __URL__ = url web interface