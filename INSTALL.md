# shorturl how to

## Install

### docker

```
$ docker-compose build
```

### virtualenv

```
$ virtualenv -p python3 --system-site-packages env
$ . ./env/bin/activate
(env) $ pip install -r requirements.txt
```

### Run

### docker

```
$ docker-compose up
```

### virtualenv

```
(env) $ ./entrypoint.sh
```

### Test

### docker

```
$ docker-compose -f docker-compose.test.yml up
```

### virtualenv

```
(env) $ python -m unittest discover
```
