FROM python:3.5.2-alpine

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="whale-linter" \
      org.label-schema.description="A simple and cross-platform Dockerfile linter" \
      org.label-schema.url="https://github.com/jeromepin/whale-linter" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/jeromepin/whale-linter" \
      org.label-schema.vendor="Jerome Pin" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"

WORKDIR /opt/whale-linter

COPY LICENSE MANIFEST.in README.md setup.py requirements.txt /opt/whale-linter/
COPY bin /opt/whale-linter/bin/
COPY whalelinter /opt/whale-linter/whalelinter/

RUN apk update \
&&  apk add ca-certificates \
&&  pip3 install -r requirements.txt \
&&  python3 setup.py install

ENTRYPOINT ["whale-linter"]

CMD ["/Dockerfile"]
