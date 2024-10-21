from flask import Flask, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    return psycopg2.connect(
        host='localhost',  # The service name of PostgreSQL container in Docker Compose
        user='root',
        password='root',
        dbname='db'
    )

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('show_users'))  # Redirect to the show_users page

    return render_template('index.html')

@app.route('/users')
def show_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, email FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('users.html', users=users)  # Pass the user data to the template

if __name__ == '__main__':
    create_tables()  # Ensure the table is created at the start
    app.run(host='0.0.0.0', port=5000)
