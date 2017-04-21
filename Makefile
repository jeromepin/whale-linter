VERSION=`grep "version =" setup.py | egrep -o '([-.0-9]+)'`

default: github pip docker-image

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
	--build-arg http_proxy='http://proxy.esrf.fr:3128' --build-arg https_proxy=http://proxy.esrf.fr:3128 \
	-t jeromepin/whale-linter:$(VERSION) .
