# Marginal tax calculator


## Usage

Two modes for running the app as follows:

### Dev mode (with debugpy)

```bash

```

### With uwsgi
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
