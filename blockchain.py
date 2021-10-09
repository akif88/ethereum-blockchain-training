from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def index(name=None):
    if name == 'patient':
        menu = ['Permission', 'View Record', 'Notification']
        return render_template('index.html', name=name, menu=menu)
    elif name == 'provider':
        menu = ['Search Patient', 'View Record with EHR System', 'View Record with Blockchain']
        return render_template('index.html', name=name, menu=menu)
    elif name == 'miner':
        menu = ['New Transaction', 'View Reward']
        return render_template('index.html', name=name, menu=menu)
    elif name is None:
        return redirect(url_for('login'))

    return render_template('index.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
