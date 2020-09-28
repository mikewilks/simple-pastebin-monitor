FROM python:3
ADD ./simple-pb-monitor.py /
RUN pip install requests slackclient
CMD [ "python","./simple-pb-monitor.py","/input","/output" ]