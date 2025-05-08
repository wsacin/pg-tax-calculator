# Marginal tax calculator

Welcome! This service provides marginal tax rate calculations based on the [tax-calculator](https://github.com/Points/interview-test-server) app.

For API details please consult the [the openapi spec](https://github.com/wsacin/pg-tax-calculator/blob/master/src/waltax/waltax.openapi.yml).

## Usage

Two modes for running the app as follows:

### Running on Dev mode (with debugpy)

```bash
python -m debugpy --listen 0.0.0.0:5678 -m flask --app waltax.app run --host=0.0.0.0 
```

### Running with uwsgi server
```bash
$ uwsgi --http 127.0.0.1:8000 --master -p 4 -w waltax.app:app
```


## Development

### Run tests
```bash

# -s to support debuging with ipdb
# -vv Verbose, especially good for assertion diffs!
$ poetry run pytest -s --vv <file> <-k test-name-pattern>
```

### Dependency management
This project uses [poetry](https://python-poetry.org/) to manage dependencies and package conflicts. Please consult the documentation to get the full benefits of poetry. For development, you can run the following:
```bash
$ pip install poetry
$ poetry install        # install dependencies on python or active virtualenv 
$ poetry update         # updates existing dependencies listed on pyproject.toml
$ poetry add <package>  # install new dependency and updates lock files
```
