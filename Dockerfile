ARG BASE_IMG=registry.gitlab.com/beerlab/cpc/utils/cps_ros_base_docker:latest

FROM ${BASE_IMG}

SHELL ["/bin/bash", "-ci"]

RUN add-apt-repository ppa:ubuntugis/ppa -y && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install gdal-bin -y &&\
    apt-get install libgdal-dev -y

RUN pip install -U pyodm opencv-python cvzone termcolor piexif
    
RUN apt-get update && \
    apt-get upgrade -y

WORKDIR /workspace/odm
COPY . /workspace/odm

ENV XDG_RUNTIME_DIR=/tmp

CMD ["/bin/bash", "-ci", "python3 continious_printer.py odm_media/results/odm_orthophoto/odm_orthophoto.tif"]
