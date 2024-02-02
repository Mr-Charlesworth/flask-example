from flask import Flask, jsonify, request, render_template, g
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'andyisawesome'


def connect_db():
    sql = sqlite3.connect('demo.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    andy = "Andy"
    return f'<h1>Hello {andy}!</h1>'


@app.route('/get-json')
def get_json():
    return jsonify({
        'key1': 'value',
        'key2': [
            1, 2, 3, 'numbers!', 4, 5, 6
        ]
    })


@app.route('/post-example', methods=['POST'])
def post_example():
    return '<h1>you made a post</h1>'


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    return data


@app.route('/send-path-param', defaults={'name': 'Default'})
@app.route('/send-path-param/<name>')
def send_path_param(name):
    return f'<h1>Hello {name}!</h1>'


@app.route('/send-query-param')
def send_query_param():
    name = request.args.get('name')
    age = request.args.get('age')
    return f'<h1>Hello {name}, you are {age} years old</h1>'


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        age = request.form['age']
        db = get_db()
        db.execute('insert into users (name, age) values (?, ?)', [name, age])
        db.commit()
        return render_template('form.html', show_result=True, name=name, age=age)
    

@app.route('/image-example')
def image_example():
  
    return render_template('img-example.html')


@app.route('/broken')
def broken():
    hidden_var = 'can you find me in the browser debugging console?'
    return undeclared_var


@app.route('/results')
def view_results():
    db = get_db()
    cur = db.execute('select id, name, age from users')
    results = cur.fetchall()
    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)