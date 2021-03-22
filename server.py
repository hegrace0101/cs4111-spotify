
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
global name
global ID
# database credentials
DATABASEURI = "postgresql://al3854:328277@34.73.36.248/project1" 

# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)

# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  #
  # example of a database query
  #
  #cursor = g.conn.execute("SELECT title, song_ID FROM song")
  ##songs = []
  #for result in cursor:
  #  songs.append(result[1])  # can also be accessed using result[0]
  #cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = songs)

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("login.html")


# Example of adding new data to the database
@app.route('/dashboard', methods=['POST'])
def dashboard():
  email = request.form['email']

  cursor = g.conn.execute('SELECT name, member_ID FROM member WHERE email = (%s)', email)
  name_tmp = []
  id_tmp = []
  for result in cursor: 
    name_tmp.append(result[0])
    id_tmp.append(result[1])
  cursor.close()
  global name
  name = name_tmp[0]
  global ID
  ID = id_tmp[0]

  return render_template("dashboard.html", name = name, id = ID)

@app.route('/followers', methods=['GET'])
def followers():

  cursor = g.conn.execute('SELECT COUNT(member_ID_1) as Number_of_Followers FROM member m, (SELECT member_id_1 FROM l_follows_m l WHERE member_ID_2 = (%s) ) as A WHERE m.member_id = a.member_id_1', ID)
  count_tmp = []
  for result in cursor: 
    count_tmp.append(result[0])
  cursor.close()
  count = count_tmp[0]

  cursor = g.conn.execute('SELECT m.name as Followers FROM member m, (SELECT member_id_1 FROM l_follows_m l WHERE member_ID_2 = (%s) ) as A WHERE m.member_id = a.member_id_1', ID)
  followers = []
  for result in cursor:
    followers.append(result[0])
  cursor.close()

  context = dict(data = followers)

  return render_template("followers.html", name = name, count = count, **context)

@app.route('/following', methods=['GET'])
def following():
  cursor = g.conn.execute('SELECT COUNT(member_ID_2) as Number_Following FROM member m, (SELECT member_id_2 FROM l_follows_m l WHERE member_ID_1 = (%s)) as A WHERE m.member_id = a.member_id_2', ID)
  count_tmp = []
  for result in cursor: 
    count_tmp.append(result[0])
  cursor.close()
  count = count_tmp[0]

  cursor = g.conn.execute('SELECT m.name as Followers FROM member m, (SELECT member_id_2 FROM l_follows_m l WHERE member_ID_1 = (%s)) as A WHERE m.member_id = a.member_id_2', ID)
  following = []
  for result in cursor:
    following.append(result[0])
  cursor.close()

  context = dict(data = following)

  return render_template("following.html", name = name, count = count, **context)

@app.route('/liked-songs', methods=['GET'])
def songs():
  cursor = g.conn.execute('SELECT COUNT(song_ID) as Number_of_Liked_Songs FROM likes WHERE member_ID LIKE (%s)', ID)
  count_tmp = []
  for result in cursor: 
    count_tmp.append(result[0])
  cursor.close()
  count = count_tmp[0]

  cursor = g.conn.execute('SELECT D.song_title as song, c.title as album, D.artist FROM (SELECT song.title as song_title, song.collection_id as album_id, C.artist FROM (SELECT B.song_id, member.name AS artist FROM (SELECT A.song_id, a_creates_s.member_ID as member_ID FROM (SELECT s.song_id AS song_id FROM likes l, song s WHERE l.member_ID = (%s) AND l.song_id = s.song_id) AS A NATURAL JOIN a_creates_s) as B NATURAL JOIN member) AS C NATURAL JOIN song) AS D LEFT OUTER JOIN collection c ON D.album_id = c.collection_id', ID)
  songs = []
  album = []
  artist = []
  for result in cursor:
    songs.append(result[0])
    album.append(result[1])
    artist.append(result[2])
  cursor.close()

  liked = {songs[i]: [album[i], artist[i]] for i in range(len(songs))}
  #context = dict(data = songs)

  return render_template("songs.html", name = name, count = count, liked = liked)

@app.route('/playlists', methods=['GET'])
def playlists():
  cursor = g.conn.execute('select c.title, c.date_created, c.duration, p.num_songs as number_of_songs, p.num_followers as Number_of_Followers from l_creates_p l, collection c, playlist p where l.member_id = (%s) AND l.collection_id = c.collection_id AND c.collection_id = p.collection_ID ', ID)
  titles = []
  date = []
  duration = []
  num_songs = []
  num_followers = []
  for result in cursor: 
    titles.append(result[0])
    date.append(result[1])
    duration.append(result[2])
    num_songs.append(result[3])
    num_followers.append(result[4])
  cursor.close()

  my_playlists = {titles[i]: [date[i], duration[i], num_songs[i], num_followers[i]] for i in range(len(titles))} 

  cursor = g.conn.execute('select c.title, c.date_created, c.duration, p.num_songs as number_of_songs, p.num_followers as Number_of_Followers, m.name from l_follows_p l, collection c, playlist p, member m where l.member_id = (%s) AND l.collection_ID = c.collection_ID AND c.collection_id = p.collection_ID AND m.member_id = l.member_id', ID)
  titles1 = []
  date1 = []
  duration1 = []
  num_songs1 = []
  for result in cursor: 
    titles1.append(result[0])
    date1.append(result[1])
    duration1.append(result[2])
    num_songs1.append(result[3])
  cursor.close()

  following_playlists = {titles1[i]: [date1[i], duration1[i], num_songs1[i]] for i in range(len(titles1))} 
  
  return render_template("playlists.html", my_playlists = my_playlists, following_playlists = following_playlists)

@app.route('/unlike', methods=['POST'])
def unlike():
  song_name = request.form['unlike']

  cursor = g.conn.execute('SELECT song_id FROM song WHERE title = (%s)', song_name)
  song_ID_tmp = []
  for result in cursor: 
    song_ID_tmp.append(result[0])
  song_ID = song_ID_tmp[0]
  cursor.close()

  g.conn.execute('DELETE from likes WHERE member_id = (%s) AND song_id = (%s)', ID, song_ID)

  return redirect('/liked-songs')

@app.route('/unfollow', methods=['POST'])
def unfollow():
  name_unfollow = request.form['unfollow']

  cursor = g.conn.execute('SELECT member_id FROM member WHERE name = (%s)', name_unfollow)
  mem_ID_unfollow_tmp = []
  for result in cursor: 
    mem_ID_unfollow_tmp.append(result[0])
  mem_ID_unfollow = mem_ID_unfollow_tmp[0]
  cursor.close()

  g.conn.execute('DELETE from l_follows_m WHERE member_id_1 = (%s) and member_ID_2 = (%s)', ID, mem_ID_unfollow)

  return redirect('/following')

@app.route('/playlist/<string:pl_name>')
def playlist(pl_name):
    name = pl_name

    cursor = g.conn.execute('SELECT collection_id FROM collection WHERE title = (%s)', name)
    playlist_ID_tmp = []
    for result in cursor:
      playlist_ID_tmp.append(result[0])
    playlist_ID = playlist_ID_tmp[0]
    cursor.close()

    cursor = g.conn.execute('select c.date_created, c.duration from playlist p, collection c where p.collection_id = c.collection_id AND c.collection_ID = (%s)', playlist_ID)
    date_tmp = []
    duration_tmp = []
    for result in cursor: 
      date_tmp.append(result[0])
      duration_tmp.append(result[1])
    date = date_tmp[0]
    duration = duration_tmp[0]

    cursor = g.conn.execute('select m.name as Creators FROM (select member_ID from l_creates_p WHERE collection_ID = (%s)) as A NATURAL JOIN member m', playlist_ID)
    creators = []
    for result in cursor: 
      creators.append(result[0])
    cursor.close()

    cursor = g.conn.execute('SELECT D.song_title as song, c.title as album, D.artist FROM (SELECT song.title as song_title, song.collection_id as album_id, C.artist FROM (SELECT B.song_id, member.name AS artist FROM  (SELECT A.song_id, a_creates_s.member_ID as member_ID FROM (SELECT p.song_id, p.collection_ID FROM s_in_p p WHERE collection_id = (%s)) AS A NATURAL JOIN a_creates_s) as B NATURAL JOIN member) AS C NATURAL JOIN song) AS D LEFT OUTER JOIN collection c ON D.album_id = c.collection_id', playlist_ID)
    songs = []
    albums = []
    artists = []
    for result in cursor:
      songs.append(result[0])
      albums.append(result[1])
      artists.append(result[2])
    cursor.close()
    
    playlist_songs = {songs[i]: [albums[i], artists[i]] for i in range(len(songs))}

    return render_template('playlist.html', name=name, date=date, duration=duration, creators=creators, songs=playlist_songs)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
