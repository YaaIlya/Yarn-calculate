import os
from flask import Flask, render_template, request, redirect, url_for, flash
from db import create_db_engine, create_session
from crud import (
    add_yarn, show_yarns, delete_yarn, delete_all_yarns, update_yarn,
    create_tables
)
from models import Yarn
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на свой секретный ключ

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/yarns_db')

# Создаем движок и сессию
engine = create_db_engine(DATABASE_URL)
session = create_session(engine)

# Создаем таблицы
create_tables(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/yarns', methods=['GET', 'POST'])
def yarns():
    if request.method == 'POST':
        brand = request.form['brand']
        name = request.form['name']
        country = request.form['country']
        color = request.form['color']
        quantity = request.form['quantity']
        
        if brand and name and country and color and quantity.isdigit():
            add_yarn(session, brand, name, country, color, int(quantity))
            flash(f'Пряжа {name} успешно добавлена!')
        else:
            flash('Пожалуйста, заполните все поля корректно.')
    
    yarns = show_yarns(session)
    return render_template('yarns.html', yarns=yarns)

@app.route('/delete_yarn/<int:yarn_id>')
def delete_yarn_route(yarn_id):
    delete_yarn(session, yarn_id)
    flash(f'Пряжа с ID {yarn_id} успешно удалена!')
    return redirect(url_for('yarns'))

@app.route('/delete_all_yarns')
def delete_all_yarns_route():
    delete_all_yarns(session)
    flash('Вся пряжа успешно удалена!')
    return redirect(url_for('yarns'))

@app.route('/update_yarn/<int:yarn_id>', methods=['POST'])
def update_yarn_route(yarn_id):
    yarn = session.query(Yarn).get(yarn_id)
    if yarn:
        brand = request.form.get('brand', yarn.brand)
        name = request.form.get('name', yarn.name)
        country = request.form.get('country', yarn.country)
        color = request.form.get('color', yarn.color)
        quantity = request.form.get('quantity', yarn.quantity)
        
        update_yarn(session, yarn_id, brand, name, country, color, int(quantity))
        flash(f'Пряжа с ID {yarn_id} успешно обновлена!')
    return redirect(url_for('yarns'))

if __name__ == '__main__':
    # Настроим хост и порт для работы в Docker-контейнере
    app.run(host='0.0.0.0', port=5000, debug=True)
