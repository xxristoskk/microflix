import requests
import csv
import time

## Reading the tsv file from imDB
data_list = []
with open('/home/xristsos/flatiron/projects/proj resources/data.tsv') as data:
    tsvreader = csv.reader(data, delimiter='\t')
    for line in tsvreader:
        data_list.append(line)

# Cleaning and parsing functions to return relavent info from the tsv file
# Function that returns items that are only movies
def type_parse(data):
    movie_list = []
    for movie in data:
        if 'movie' in movie:
            movie_list.append(movie)
        else:
            continue
    return movie_list

# Function that removes all movies that have not been released yet
def release_parse(data):
    movie_list = []
    for movie in data:
        if movie[6] == '\\N':
            data.remove(movie)
    return movie_list

## Function that parses through tsv data by year and type
def clean_data(data):
    clean_list = []
    # Loop that only returns movies between 2010 and 2019
    for x in data:
        if '2010' in x:
            clean_list.append(x)
        elif '2011' in x:
            clean_list.append(x)
        elif '2012' in x:
            clean_list.append(x)
        elif '2013' in x:
            clean_list.append(x)
        elif '2014' in x:
            clean_list.append(x)
        elif '2015' in x:
            clean_list.append(x)
        elif '2016' in x:
            clean_list.append(x)
        elif '2017' in x:
            clean_list.append(x)
        elif '2018' in x:
            clean_list.append(x)
        elif '2019' in x:
            clean_list.append(x)
        else:
            continue
    return clean_list

## omDB only returns 1 movie at a time and allows 1000 requests per day
## To get the most out of the imDB tsv, the code below breaks up the clean_list
clean_data = type_parse(clean_data(data_list))
test_list = []
for x in range(1000):
    test_list.append(clean_data[x])
id_list = []
for x in test_list:
    id_list.append(x[0])

## Calls the omDB API with an imDB id number and returns the movie info in a json file
def _omdb(url, id_, api):
    response = requests.get(url + '?i=' + id_ + api)
    data = response.json()
    return data

## Takes in a list of imDB movie IDs
## Returns a list of dictionaries
def collect_and_clean(data):
    movie_list = []
    for movie in data:
        movie_list.append(_omdb(url, movie, omdb_api))
    for movie in movie_list:
        try:
            if movie['Genre'] == "N/A":
                movie_list.remove(movie)
        except:
            movie_list.remove(movie)
    for movie in movie_list:
        try:
            movie['Year'] = int(movie['Year'])
        except:
            movie_list.remove(movie)
        try:
            if movie['Year'] >= 2005 and movie['Year'] <= 2019:
                continue
            else:
                movie_list.remove(movie)
        except:
            movie_list.remove(movie)
    for movie in movie_list:
        try:
            if 'English' not in movie['Language']:
                movie_list.remove(movie)
            else:
                continue
        except:
            movie_list.remove(movie)
    for movie in movie_list:
        try:
            if movie['Released'] == 'N/A':
                movie_list.remove(movie)
            else:
                continue
        except:
            movie_list.remove(movie)
    time.sleep(5)
    return movie_list

## Sending the info into the database
import requests
import mysql.connector
from mysql.connector import errorcode
import json

## Connect to DB server on AWS
cnx = mysql.connector .connect(
    host = config.host,
    user = config.user,
    passwd = config.passwd)
cursor = cnx.cursor()

#create table
cursor.execute(
              """CREATE TABLE microflix.imdb (
              id int AUTO_INCREMENT,
              movie varchar(250),
              actors varchar(1000),
              released varchar(50),
              genre varchar(500),
              boxoffice varchar(500),
              director varchar(500),
              PRIMARY KEY (id)
              )""")

#inserting movies into the table
def insert_movies(movies):
    for movie in movies:
        if movie['Response'] == 'False':
            continue
        else:
            sql_add = ("""INSERT INTO microflix.imdb (movie, actors, released, genre, boxoffice, director) VALUES (%s, %s, %s, %s, %s, %s)""")
            data_add = (movie['Title'], movie['Actors'], movie['Released'], movie['Genre'], movie['BoxOffice'], movie['Director'])
            cursor.execute(sql_add, data_add)
    cursor.close()
    cnx.commit()
    return