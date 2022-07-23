from flask import Flask, render_template, url_for, request, flash, g
from func import change_info, fun_clean_wall, gift_sender
from FDataBase import FDataBase
import sqlite3
import os

DATABASE = '/tmp/flask_vk.db'
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'ghyedcvnkhgffgjkjh'

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask_vk.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.route('/')
@app.route('/index')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', posts=dbase.getPosts())

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    print(get_db())
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        res = dbase.addPost(request.form['name'], request.form['post'])
        if not res:
            flash('Ошибка добавления')
        else:
            flash('Добавлено')
    return render_template("add_post.html")


@app.route('/change_info_accs', methods=['POST', 'GET'])
def change_info_accs():
    if request.method == 'POST':
        accs = request.form.get('accs')
        if accs and ":" in accs:
            accs = accs.split()
            print(accs)
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            countre = request.form.get('countre')
            city = request.form.get('city')
            sex = request.form.get('sex')
            relation = request.form.get('relation')
            status = request.form.get('status')
            log = change_info(accs, first_name=first_name, last_name=last_name,
                              city=city, countre=countre, status=status)
            return render_template('change_info_accs.html', accs=accs,
                                   first_name=first_name, last_name=last_name,
                                   countre=countre, city=city, log=log,
                                   sex=sex, relation=relation)
        flash("Неверные данные в логин и пароль")
        return render_template('change_info_accs.html')
    else:
        return render_template('change_info_accs.html')

@app.route('/clean_wall', methods=['POST', 'GET'])
def clean_wall():
    account = request.form.get('account')
    if request.method == 'POST':
        print(account)
        flash(fun_clean_wall(account))
        return render_template('clean_wall.html')
    else:
        return render_template('clean_wall.html')

@app.route('/gift_send', methods=['POST', 'GET'])
def gift_send():
    if request.method == 'POST':
        accs = request.form.get('accounts')
        print(accs)
        if accs and ':' in accs:
            accs = accs.split()
            id_user = request.form.get('user')
            id_gift = request.form.get('gift')
            anon = request.form.get('anon')
            one = request.form.get('one')
            message = request.form.get('message')
            flash(gift_sender(accs, id_user, id_gift, anon, one, message))
            return render_template('gift_send.html')
        return render_template('gift_send.html')
    else:
        return render_template('gift_send.html')

if __name__ == '__main__':
    app.run(debug=True)