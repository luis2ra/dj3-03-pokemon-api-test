# dj3-03-pokemon-api-test

Pokemon API testing application from the [PokeApi](https://pokeapi.co/)

### Dependencies

- Django==3.1
- djangorestframework==3.11.0
- requests==2.26.0
- django-environ==0.7.0

### Installation

1. Clone this project:

```sh
$ git clone https://github.com/luis2ra/dj3-03-pokemon-api-test.git
```

2. Generate .env file (view example file)


3. Install the dependencies and start the server.

```sh
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```


### Using dj3-03-pokemon-api-test

For fetch and store the pokemons data:

```sh
$ python manage.py evolution_chain <id>
```

To obtain the data saved locally of the pokemons or of a single pokemon (passing the name), invoke in the navigator:

```sh
http://127.0.0.1:8000/api/pokemons/

http://127.0.0.1:8000/api/pokemon/<name>
```
