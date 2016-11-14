
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)


#set up DB
mysql = MySQL()

app.config['MYSQL_USER'] = 'user1'
app.config['MYSQL_PASSWORD'] = '0Database!'
app.config['MYSQL_DB'] = 'MoviePal'
app.config['MYSQL_HOST'] = 'localhost'

mysql.init_app(app)


#global for now, change later
movie_ids = []
movie_titles = []

@app.route('/')
def main():
  #store movie_titles and ids somewhere
  global movie_ids, movie_titles
  movies = list(users())
  movie_id_list = [str(i[0]) for i in movies]
  movie_ids = movie_id_list
  movie_title_list = [str(i[1]) for i in movies]
  movie_titles = movie_title_list
  return render_template('index.html', movies = zip(movie_ids,movie_titles))

def users():
  cur = mysql.connection.cursor()
  cur.execute('''SELECT table1.movie_id,title from movie as table1 inner join 
                (SELECT movie_id, COUNT(*) AS magnitude  FROM UserRating  GROUP BY movie_id  ORDER BY magnitude DESC LIMIT 10) 
                as table2 ON (table1.movie_id = table2.movie_id)''')
  movies = cur.fetchall()
  return movies

@app.route('/recommendations', methods=['POST'])
def recommendations():
  #maps movie_ids to ratings
  ratings = {}
  for id in movie_ids:
    ratings[id] = int(request.form.get(id))

  #Generate recommendations using ratings
  generateRecommendations(ratings)
  return render_template('recommendations.html')

def generateRecommendations(ratings):
  #keep only non-zero entries
  ratings = {k:v for k,v in ratings.items() if v != 0}

if __name__ == "__main__":
  app.run()
