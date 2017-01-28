default:
	@docker build \
	--build-arg VCS_REF=`git rev-parse --short HEAD` \
	--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
	--build-arg VERSION=`grep "version =" setup.py | egrep -o '([-.0-9]+)'` \
	-t jeromepin/whale-linter:`grep "version =" setup.py | egrep -o '([-.0-9]+)'` .
