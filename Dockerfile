
# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first


# create root directory for our project in the container
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /icecream
RUN apt-get update

# Set the working directory to /filmsanj
WORKDIR /icecream

# Copy the current directory contents into the container at /icecream
ADD . /icecream/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

