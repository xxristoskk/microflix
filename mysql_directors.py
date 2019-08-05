## Sending the info into the database
import requests
import mysql.connector
from mysql.connector import errorcode
import json
import matplotlib.pyplot as plt
%matplotlib inline

## Connect to DB server on AWS
cnx = mysql.connector .connect(
    host = 'flatiron.clnl5ba3xlkw.us-east-2.rds.amazonaws.com',
    user = 'xristos2',
    passwd = '')
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
insert_movies(final_list2)

## SQL Queries
cursor.execute('''SELECT DISTINCT director, person_name, popularity, movie FROM microflix.imdb
                  JOIN microflix.popular_people
                  ON microflix.imdb.movie = microflix.popular_people.title
                  ORDER BY popularity DESC''')

results = cursor.fetchall()

## Preparing query results for plotting
r_list = []
for x in results:
    r_dict = {'director': x[0], 'actor': x[1], 'popularity': x[2], 'movie': x[3]}
    r_list.append(r_dict)
x = []
y = []
for i in r_list:
    y.append(i['popularity'])
    x.append(i['director'])

## Crating bar graph
fig, ax = plt.subplots()
ax.barh(x,y,color='green')
ax.set_title('Director popularity')
ax.set_xlabel('Popularity')
ax.set_ylabel('Directors')
fig
fig.savefig('directorpop1.png',bbox_inches='tight')
