#!/bin/bash

docker build -t student_search_i .
docker run -it --name student_search_c student_search_i bash
