# Advised run command: docker run -p 52022:22 -d --restart unless-stopped --name adventure -v path/to/data:/app/data adventure

FROM python:3.7

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd

# Don't need a message of the day
RUN rm /etc/motd

# Add user mprog with password student
RUN echo 'root:student' | chpasswd root

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22

# Add current directory to the app folder
COPY ./app.py  /app/
COPY ./classes/* /app/classes/
COPY ./requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && rm -rf ~/.cache/pip

RUN chsh -s /app/app.py root

CMD ["/usr/sbin/sshd", "-D"]
