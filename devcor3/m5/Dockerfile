# Start with this excellent all-in-one ELK stack container
# https://elk-docker.readthedocs.io/
FROM sebp/elk:latest

# Update the maintainer label for this specific image
LABEL maintainer="njrusmc.net"

# Additionally accept JSON logs from Python over basic TCP. Just add
# a new configuration file to logstash, enabling the new port.
COPY ./03-tcp-input.conf /etc/logstash/conf.d/03-tcp-input.conf
