import sqlite3

from testdb import get_db

from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=('GET', 'POST'))
def insert_db():

    if request.method == 'POST':
        ida = request.form['id']
        user_id = request.form['username']
        password = request.form['password']
        error = None
        print(ida)
        if not user_id:
            error = 'Error!!!'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('INSERT INTO user VALUES (?,?,?)', (int(ida), user_id, password))
            db.commit()
            return redirect(url_for('index'))

    return render_template('signup.html')


if __name__ == "__main__":
    app.run()







 
