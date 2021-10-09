from flask import Flask, render_template
import sqlite3

from testdb import init_db, close_connection

app = Flask(__name__)

'''
    using sqlite3 with flask => http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
                                https://github.com/pallets/flask/tree/master/examples/tutorial
                                
    sqlite3 cli command      => https://www.sqlite.org/cli.html
                                https://www.sqlite.org/lang.html (SQL)
'''


@app.route('/')
def hello():
    post = 'asd' # to use as a variable in hmtl 
    return render_template('index.html', posts = post)


@app.route('/content')
def content():
    return render_template('content.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run()
    init_db()
    close_connection()


