FROM python:3
ADD simple_pb_monitor.py /
RUN pip install requests slackclient
CMD [ "python","./simple_pb_monitor.py","/input","/output" ]