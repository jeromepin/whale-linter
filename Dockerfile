FROM python:3.5.2-alpine

MAINTAINER Jerome Pin <jerome@jeromepin.fr>

WORKDIR /opt/whale-linter

COPY LICENSE MANIFEST.in README.md setup.py /opt/whale-linter/
COPY bin /opt/whale-linter/bin/
COPY whalelinter /opt/whale-linter/whalelinter/

RUN python3 setup.py install

ENTRYPOINT ["whale-linter"]

CMD ["/Dockerfile"]
