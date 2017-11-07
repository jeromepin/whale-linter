VERSION=`grep "version =" setup.py | egrep -o '([-.0-9]+)'`

default: build

tests:
	python3 tests.py

build:
	python3 setup.py install --user >> /dev/null

publish: github

github:
	git tag --force $(VERSION) && \
	git push && \
	git push --tags
