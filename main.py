import sqlite3, datetime
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('stats.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    conn = get_db_connection()
    row = conn.execute("SELECT pet_name, cost FROM pet WHERE discord_id = 0").fetchone()
    conn.close()
    return render_template('home.html', row=row)


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    
    if request.method == 'POST':
        trans_id = request.form.get('trans_id')
        username = request.form.get('username')
        trans_type = request.form.get('trans_type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')

        if trans_id:
            query += ' AND discord_id = ?'
            params.append(trans_id)
        if username:
            query += ' AND username LIKE ?'
            params.append(f'%{username}%')
        if trans_type:
            query += ' AND type = ?'
            params.append(trans_type)
        if start_date and start_time:
            start_datetime = f"{start_date} {start_time}:00"
            query += " AND created_at >= ?"
            params.append(start_datetime)
        if end_date and end_time:
            end_datetime = f"{end_date} {end_time}:59"
            query += " AND created_at <= ?"
            params.append(end_datetime)
        if start_date:
            query += ' AND created_at >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND created_at <= ?'
            params.append(end_date)
    else:
        query = "SELECT * FROM transactions WHERE created_at LIKE ?"
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        params = [f'{today}%']
    
    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('transactions.html', rows=rows)


@app.route('/users', methods=['GET', 'POST'])
def users():
    query = '''SELECT u.discord_id, u.balance, COALESCE(un.username, 'Unknown') AS username
    FROM users u
    LEFT JOIN user_name un ON u.discord_id = un.discord_id WHERE 1=1'''
    params = []

    if request.method == 'POST':
        discord_id = request.form.get('discord_id')
        username = request.form.get('username')
        balance = request.form.get('balance')

        if discord_id:
            query += ' AND u.discord_id = ?'
            params.append(discord_id)
        if username:
            query += ' AND un.username LIKE ?'
            params.append(f'%{username}%')
        if balance:
            query += ' AND u.balance >= ?'
            params.append(balance)


    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('users.html', rows=rows)


@app.route('/stats', methods=['GET', 'POST'])
def stats():
    query = "SELECT * FROM stats WHERE 1=1"
    params = []

    if request.method == 'POST':
        stat_name = request.form.get('stat_name')
        count = request.form.get('count')

        if stat_name:
            query += ' AND stat_name LIKE ?'
            params.append(f'%{stat_name}%')
        if count:
            query += ' AND count >= ?'
            params.append(count)


    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('stats.html', rows=rows)


@app.route('/upgrades', methods=['GET', 'POST'])
def upgrades():
    query = '''SELECT u.user_id, u.upgrade_name, u.upgrade_level, COALESCE(un.username, 'Unknown') AS username
    FROM upgrades u
    LEFT JOIN user_name un ON u.user_id = un.discord_id WHERE 1=1'''
    params = []

    if request.method == 'POST':
        discord_id = request.form.get('discord_id')
        upgrade_name = request.form.get('upgrade_name')
        upgrade_level = request.form.get('upgrade_level')
        username = request.form.get('username')

        if discord_id:
            query += ' AND user_id = ?'
            params.append(discord_id)
        if upgrade_name:
            query += ' AND upgrade_name LIKE ?'
            params.append(f'%{upgrade_name}%')
        if upgrade_level:
            query += ' AND upgrade_level = ?'
            params.append(upgrade_level)
        if username:
            query += ' AND un.username LIKE ?'
            params.append(f'%{username}%')


    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('upgrades.html', rows=rows)


@app.route('/fortune', methods=['GET', 'POST'])
def fortune():
    query = '''SELECT f.discord_id, f.count, COALESCE(un.username, 'Unknown') AS username
    FROM fortune f
    LEFT JOIN user_name un ON f.discord_id = un.discord_id WHERE 1=1'''
    params = []

    if request.method == 'POST':
        discord_id = request.form.get('discord_id')
        username = request.form.get('username')
        count = request.form.get('count')

        if discord_id:
            query += ' AND discord_id = ?'
            params.append(discord_id)
        if count:
            query += ' AND count >= ?'
            params.append(count)
        if username:
            query += ' AND un.username LIKE ?'
            params.append(f'%{username}%')


    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('fortune.html', rows=rows)


@app.route('/networth', methods=['GET', 'POST'])
def networth():
    query = '''SELECT u.discord_id, u.networth, COALESCE(un.username, 'Unknown') AS username
    FROM user_networth u 
    LEFT JOIN user_name un ON u.discord_id = un.discord_id WHERE 1=1'''
    params = []

    if request.method == 'POST':
        discord_id = request.form.get('discord_id')
        username = request.form.get('username')
        networth = request.form.get('networth')

        if discord_id:
            query += ' AND discord_id = ?'
            params.append(discord_id)
        if networth:
            query += ' AND networth >= ?'
            params.append(networth)
        if username:
            query += ' AND un.username LIKE ?'
            params.append(f'%{username}%')


    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('networth.html', rows=rows)


@app.route('/pets', methods=['GET', 'POST'])
def pets():
    query = '''SELECT p.discord_id, p.pet_name, p.count, p.cost, COALESCE(un.username, 'Unknown') AS username
    FROM pet p
    LEFT JOIN user_name un ON p.discord_id = un.discord_id WHERE 1=1'''
    params = []

    if request.method == 'POST':
        discord_id = request.form.get('discord_id')
        pet_name = request.form.get('pet_name')
        username = request.form.get('username')
        count = request.form.get('count')
        cost = request.form.get('cost')

        if discord_id:
            query += ' AND discord_id = ?'
            params.append(discord_id)
        if pet_name:
            query += ' AND pet_name LIKE ?'
            params.append(f'%{pet_name}%')
        if count:
            query += ' AND count >= ?'
            params.append(count)
        if cost:
            query += ' AND cost >= ?'
            params.append(cost)
        if username:
            query += ' AND un.username LIKE ?'
            params.append(f'%{username}%')


    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('pets.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
