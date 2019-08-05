import requests
import csv
import time
import config

url = "http://www.omdbapi.com/"
omdb_api = config.omdb_api

## Reading the tsv file from imDB containing over 6 million titles
data_list = []
with open('/home/xristsos/flatiron/projects/proj resources/data.tsv') as data:
    tsvreader = csv.reader(data, delimiter='\t')
    for line in tsvreader:
        data_list.append(line)

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

## Create a clean and parsed data list
clean_data = type_parse(clean_data(data_list))

## Collect all the movie IDs in a list
temp_list = []
for x in range(12000):
    temp_list.append(clean_data[x])
id_list = []
for x in temp_list:
    id_list.append(x[0])

## Calls the omDB API with an imDB movie id and returns the movie info in a json file
def _omdb(url, id_, api):
    response = requests.get(url + '?i=' + id_ + api)
    data = response.json()
    return data

## Takes in a list of imdb IDs and returns a list of dictionaries for each movie
def collect_and_clean(data):
    movie_list = []
    for movie in data:
        movie_list.append(_omdb(url, movie, omdb_api))
    for movie in movie_list:
        ## Checks if any dictionary keys are missing and removes item from the list
        try:
            ## Change years from strings to integers
            movie['Year'] = int(movie['Year'])
            if movie['Year'] >= 2005 and movie['Year'] <= 2019:
                continue
            else:
                movie_list.remove(movie)
            ## Remove the movie if it has no genre data
            if movie['Genre'] == "N/A":
                movie_list.remove(movie)
            ## Remove movie if it is not in English
            if 'English' not in movie['Language']:
                movie_list.remove(movie)
            else:
                continue
            ## Remove the movie if it has not been released
            if movie['Released'] == 'N/A':
                movie_list.remove(movie)
            else:
                continue
        except:
            movie_list.remove(movie)
    time.sleep(2)
    return movie_list
