# Begin with a lightweight Python 3.7.3 container, which is the same
# version we used for our development. Alpine Linux is a minimal
# distribution and is popular for containerized apps.
FROM python:3.7.3-alpine
LABEL maintainer="njrusmc@gmail.com"

# Shell commands to execute after basic Python 3.7 container
# is deployed. We only need to install flash for this app.
RUN pip install flask

# Change into the correct directory. WORKDIR is the Docker best practice
# versus "RUN cd /src" as it is cleaner and more explicit.
WORKDIR /src

# Flash default HTTP port is TCP 5000 in the CRM app. This doesn't actually
# publicly expose the port but serves as a useful reference.
EXPOSE 5000/tcp

# Run the program by starting flask
ENTRYPOINT ["python"]
CMD ["start.py"]
