FROM postgres:13-alpine

EXPOSE ${POSTGRES_PORT}

COPY initdb/ /docker-entrypoint-initdb.d/

CMD ["postgres"]
