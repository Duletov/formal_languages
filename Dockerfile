FROM graphblas/pygraphblas-minimal:v3.3.3

ARG mod
ENV mod ${mod}
ARG graph
ENV graph ${graph}
ARG query
ENV query ${query}
ARG start
ENV start ${start}
ARG end
ENV end ${end}

RUN mkdir /assignment_1
WORKDIR /assignment_1
COPY . /assignment_1

RUN pip3 install -r minimal-requirements.txt
RUN python3 -m pytest -v -s
CMD if [ "x$start" = "x" ] ; then python3 main.py --mod $mod --graph $graph --query $query ; else if [ "x$end" = "x" ] ; then python3 main.py --graph $graph --query $query --start $start ; else python3 main.py --graph $graph --query $query --start $start --end $end ; fi ; fi