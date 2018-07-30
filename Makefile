all: help

help:
	echo 'try make build'

doc:
	./build_docs.py

build:
	./build_package.py

install: build doc
	./release_package.py

conform:
	/usr/bin/env PYTHONPATH=`pwd`/fc14/python:$$PYTHONPATH:/spin/software/spinasset/0.19.0/python:/spin/software/spin3d/2.17.1/python:/spin/software/spinlaunch/0.42.0/python ./pylint spin2d

clean:
	rm -rf build
	rm -rf doc/_api

.PHONY: build doc install clean help
