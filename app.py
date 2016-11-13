
from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_USER'] = 'user1'
app.config['MYSQL_PASSWORD'] = '0Database!'
app.config['MYSQL_DB'] = 'MoviePal'
app.config['MYSQL_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/')
def main():
  #tuple
  movies = list(users())
  movie_titles = [str(i[0]) for i in movies]
  print(movie_titles)
  return render_template('index.html', movies = movie_titles)

def users():
  cur = mysql.connection.cursor()
  #cur.execute('''SELECT * FROM movie limit 10''')
  cur.execute('''SELECT title from movie as table1 inner join 
                (SELECT movie_id, COUNT(*) AS magnitude  FROM UserRating  GROUP BY movie_id  ORDER BY magnitude DESC LIMIT 10) 
                as table2 ON (table1.movie_id = table2.movie_id)''')
  movies = cur.fetchall()
  return movies

if __name__ == "__main__":
  app.run()
