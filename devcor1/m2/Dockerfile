# Begin with a minimal Alpine Linux Python 3.7.3 container, which is the
# same version we used for our development.
FROM python:3.7.3-alpine
LABEL maintainer="njrusmc@gmail.com"

# Shell commands to execute after basic Python 3.7 container
# is deployed. We only need to install flask for this app.
RUN pip install flask
#
# Rather than use a bind mount, we can also package our source code
# with the container. This makes CD via k8s easier.
COPY src /src

# Change into the correct directory. WORKDIR is the Docker best practice
# versus "RUN cd /src" as it is cleaner and more explicit.
WORKDIR /src

# Flask default HTTP port is TCP 5000 in the CRM app. This doesn't actually
# publicly expose the port but serves as a useful reference.
EXPOSE 5000/tcp

# Run the program by starting flask
ENTRYPOINT ["python"]
CMD ["start.py"]
