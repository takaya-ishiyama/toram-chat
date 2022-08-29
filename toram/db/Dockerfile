FROM postgres:9.6.9-alpine
COPY postgresql.conf /etc/postgresql.conf
ADD init_db.sh .
RUN chown postgres /etc/postgresql.conf
