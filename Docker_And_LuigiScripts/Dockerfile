FROM ubuntu:14.04

RUN apt-get update

RUN apt-get -y install python3  

RUN apt-get -y install python3-pip wget curl libssl-dev

RUN apt-get -y install software-properties-common 
RUN add-apt-repository ppa:git-core/ppa

ENV PYTHON_PIP_VERSION 9.0.1

RUN pip3 install --upgrade --force-reinstall "pip==$PYTHON_PIP_VERSION"

MAINTAINER Team6

RUN apt-get update

RUN mkdir /Docker_Luigi

RUN mkdir /Docker_Files

ADD requirements.txt /Docker_Luigi/requirements.txt

RUN pip3 install -r /Docker_Luigi/requirements.txt

ADD ./FinalProject_Luigi.py /Docker_Luigi

ADD ./FinalProject_DataDownload.py /Docker_Luigi

WORKDIR /Docker_Luigi

CMD python3 -m luigi --module FinalProject_Luigi PredictAndForecast --awsaccesskeyid $accesskey --awssecretaccesskey $secretkey --local-scheduler --bucketName $bucket
