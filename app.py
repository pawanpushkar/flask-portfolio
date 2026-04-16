from flask import Flask,render_template,request,Response
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        conn = sqlite3.connect('contact.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, email, message) VALUES (?,?,?)",(name,email,message))

        conn.commit()
        conn.close()
        return render_template('contact1.html', success=True)
    return render_template('contact1.html',success=False)

@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/resume')
def resume():
    return render_template('resume1.html')

@app.route('/admin/messages')
def admin_messages():
    auth = request.authorization
    if not auth or not (auth.username == 'Admin' and auth.password == 'admin1234'):
        return Response(
            'Login required',401,
            {'WWW-Authenticate':'Basic realm="Admin Login"'}
        )

    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, message, submitted_at FROM messages ORDER BY submitted_at DESC")
    messages = cursor.fetchall()
    conn.close()
    return render_template('admin_messages.html', messages=messages)


if __name__ == '__main__':

    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

    app.run(debug=True)