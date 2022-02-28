import requests
from flask import Flask, render_template, request, redirect
import psycopg2
from config import host, user, passw, db_name, porte

# Создаем приложение
app = Flask(__name__)
# подключение к базе данных
conn = psycopg2.connect(database=db_name,
                        user=user,
                        password=passw,
                        host=host,
                        port=porte)

# Добавляем курсор для обращения к базе данных
cursor = conn.cursor()
cursor2 = conn.cursor()


# Создаем первый декоратор
@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if str(username) == '' or str(password) == '':
                return render_template('account.html', full_name='Error (enter login and password)')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if records:
                return render_template('account.html', full_name='Hello, ' + records[0][1],
                                       log_pas='Password = ' + records[0][2] + ', Login = ' + records[0][3])
            else:
                return render_template('account.html', full_name='User not found')
        elif request.form.get("registration"):
            return redirect("/registration/")


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if name == '' or login == '' or password == '': return render_template('registration.html')
        cursor2.execute("SELECT * FROM service.users WHERE login='{log}'".format(log=str(login)))
        if not list(cursor2.fetchall()):
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',
                           (str(name), str(login), str(password)))
        else: return render_template('registration.html')
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')
