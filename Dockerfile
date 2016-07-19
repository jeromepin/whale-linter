FROM python:3.5.2-alpine

MAINTAINER Jerome Pin <jerome@jeromepin.fr>

RUN pip3 install whalelinter

ENTRYPOINT ["whale-linter"]

CMD ["/Dockerfile"]
