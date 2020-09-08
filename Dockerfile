FROM graphblas/pygraphblas-minimal:latest

RUN mkdir /assignment_1
WORKDIR /assignment_1
COPY . /assignment_1

RUN pip3 install -r minimal-requirements.txt
CMD ["pytest"]
