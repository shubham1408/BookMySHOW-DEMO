# BOOKMYSHOW DEMO
==================================

This is an asignment codebase which includes apis with unit test cases.

All post APIs are session authenticated and browsable apis and GET apis
are public APIs

# URLS FOR APIS (APIS ARE BROWSABLE)

  1. Ability to view all the movies playing in your city

      ----localhost:port_number(8000)/api/movie/city/?city=city_name----

  2. Ability to check all cinemas in which a movie is playing along with all the showtimes
      
      ----localhost:port_number(8000)/api/cinema/movie/?movie=movie_name----
  
  3. For each showtime, check the availability of seats

  	  ----localhost:port_number(8000)/api/seats/by/show_time/?show_time=query_time----
    	
    	QUERY TIME SHOULD BE IN ISO FORMAT
    	for example:- "2020-04-03T09:38:10.438740Z"

  4. User Sign up and login

  	  ----localhost:port_number(8000)/api/user/signup/----(SIGNUP API)
  	  ----localhost:port_number(8000)/api-auth/login/----(LOGIN API)

  5. Ability to book a ticket. (No payment gateway integration is required. 
     Assume tickets can be booked for free)

     ----localhost:port_number(8000)/api/book/ticket/----


# Technology Stack

  Python == 3.6.8
  
  Django == 3.0.5 

  Djangorestframework == 3.11.0
  
  MySql == 5.7.29

# Installation

## Install OS (Ubuntu) Requirements

    sudo apt-get update
    sudo apt-get upgrade

## Clone Project

    git clone https://github.com/shubham1408/BookMySHOW-DEMO.git

## Setup your virtual environment and install requirements.

### Ubuntu/Mac setup

    python3 -m venv convenv
    source convenv/bin/activate
    pip3 install -r convo/convo/requirements.txt
    

## MySQL (database) setup

    sudo apt-get install mysql-server
    mysql -u root -p (for Ubuntu, you might need to run it as sudo mysql -u root -p)
    create database convodb;
    grant usage on *.* to myuser@localhost identified by 'mypasswd';
    grant all privileges on convodb.* to myuser@localhost;

obtain a dump of the database (convodb.sql from convo/convodb.sql) and then add it to your local MySQL server  (ensure that you run MySQL from the directory with the dump file):

    use convodb;
    source convodb.sql;

## Running Development Server

   python manage.py runserver


## Runninng ALL Test CASES

   python manage.py test


**Note:** Never forget to enable virtual environment (`source convenv/bin/activate`) before running the above commands and use settings accordingly.

