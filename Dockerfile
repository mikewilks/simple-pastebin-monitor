FROM python:3
ADD ./simple-pb-monitor.py /
RUN pip install requests
CMD [ "python","./simple-pb-monitor.py","/input/keywords.txt","/output", "False" ]