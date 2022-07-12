from flask import Flask, render_template, url_for, request, flash
from func import change_info, fun_clean_wall


app = Flask(__name__)
app.secret_key = 'ghyedcvnkhgffgjkjh'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)