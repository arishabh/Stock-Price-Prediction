ROM ubuntu:latest
MAINTAINER Rishabh Agrawal <ragrawa@iu.edu>

RUN apt-get update -y
RUN apt-get install -y apt-utils

RUN apt-get install -y build-essential libssl-dev

RUN apt-get install -y git-core
RUN apt-get install -y dnsutils
RUN apt-get install -y curl
RUN apt install -y python3.7

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 10
RUN update-alternatives --config python

RUN apt-get install -y python3.7-distutils
RUN apt-get install -y python3.7-dev


RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py 

RUN pip install -U pip setuptools
RUN pip install psutil

RUN git clone https://github.iu.edu/ise-engr-e222/sp20-id-0019.git

RUN cd .. git pull 

WORKDIR ise-engr-e222/sp20-id-0019/project/project-code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install connexion[swagger-ui]

EXPOSE 8000

CMD ["make", "start"]

