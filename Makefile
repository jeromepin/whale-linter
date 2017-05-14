VERSION=`grep "version =" setup.py | egrep -o '([-.0-9]+)'`

default: build

tests:
	python3 tests.py

build:
	python3 setup.py install --user >> /dev/null

publish: github pip docker-image

github:
	git tag --force $(VERSION) && \
	git push && \
	git push --tags

pip:
	python3 setup.py register -r pypi && \
	python3 setup.py sdist upload -r pypi

docker-image:
	@docker build \
	--build-arg VCS_REF=`git rev-parse --short HEAD` \
	--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
	--build-arg VERSION=$(VERSION) \
	-t jeromepin/whale-linter:$(VERSION) .
