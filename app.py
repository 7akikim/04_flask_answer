import os
from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from models import db, Movie
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_flask.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# sqlalchemy 초기화
db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'movies'
    # __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    title_en = db.Column(db.String, nullable=False)
    audience = db.Column(db.Integer, nullable=False)
    open_date = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    watch_grade = db.Column(db.String, nullable=False)
    score = db.Column(db.Float, nullable=False)
    poster_url = db.Column(db.String, nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    
    def __repr__(self):
        return f"<Movie '{self.id}: {self.title}'>"

migrate = Migrate(app, db)


@app.route('/movies/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movies/new/')
def new():
    return render_template('new.html')


@app.route('/movies/create/')
def create():
    # 재석이 화이팅!!!!!
    
    movie = Movie(**request.args)
    # title = request.args.get('title')
    # title_en = request.args.get('title_en')
    # audience = request.args.get('audience')
    # open_date = request.args.get('open_date')
    # genre = request.args.get('genre')
    # watch_grade = request.args.get('watch_grade')
    # score = request.args.get('score')
    # poster_url = request.args.get('poster_url')
    # description = request.args.get('description')

    # movie = Movie(title=title, title_en=title_en,
    #             audience=audience, open_date=open_date,
    #             genre=genre, watch_grade=watch_grade,
    #             score=score, poster_url=poster_url,
    #             description=description)

    db.session.add(movie)
    db.session.commit()
    return redirect(f'/movies/{movie.id}/')

@app.route('/movies/<int:id>/')
def show(id):
    movie = Movie.query.get(id)
    return render_template("show.html", movie=movie)

@app.route('/movies/<int:id>/edit/')
def edit(id):
    movie = Movie.query.get(id)
    return render_template("edit.html", movie=movie)

@app.route('/movies/<int:id>/update/')
def update(id):
    print(request.args)
    movie = Movie.query.get(id)
    # 재석이 화이팅22222!!!!!
    for column, value in request.args.items():
        setattr(movie, column, value)
        #  대체가능 movie[column] = value
    # title = request.args.get('title')
    # title_en = request.args.get('title_en')
    # audience = request.args.get('audience')
    # open_date = request.args.get('open_date')
    # genre = request.args.get('genre')
    # watch_grade = request.args.get('watch_grade')
    # score = request.args.get('score')
    # poster_url = request.args.get('poster_url')
    # description = request.args.get('description')

    # movie.title = title
    # movie.title_en = title_en
    # movie.audience = audience
    # movie.open_date = open_date
    # movie.genre = genre
    # movie.watch_grade = watch_grade
    # movie.score = score
    # movie.poster_url = poster_url
    # movie.description = description
    db.session.commit()
    return redirect(f'/movies/{movie.id}/')

@app.route('/movies/<int:id>/delete/')
def delete(id):
    movie = Movie.query.get(id)

    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    # app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True)
    app.run(host='0.0.0.0', port='8080', debug=True)