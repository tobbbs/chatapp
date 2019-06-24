from flask import Flask, render_template, request, redirect, make_response
import sqlite3
import json

conn = sqlite3.connect("data/chatroom.db")
conn.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username text not null, password text not null)');
conn.execute('CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT, body text not null, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id) )');
conn.commit()
conn.close()

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/random')
def random():
    return 'random'

@app.route('/register',methods = ['POST', 'GET'])
def register():
    with sqlite3.connect("data/chatroom.db") as conn:
        c = conn.cursor()
        if request.method == 'POST':
            new_username = request.form["input_username"]
            new_password = request.form["input_password"]
            c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()
            resp = make_response(redirect("/", code=302))
            resp.set_cookie('username', new_username)
            return resp 
        return render_template("register.html")

@app.route('/chatroom', methods=["GET","POST"])
def retrieve():
    print(request.get_data())
    print(request.form)
    with sqlite3.connect("data/chatroom.db") as conn:
        c = conn.cursor()
        name = request.cookies.get('username')
        if request.method == "GET":
            all_messages = c.execute("SELECT username, body FROM users, messages WHERE users.id=user_id").fetchall()
            print(all_messages)
            return json.dumps(all_messages)
        else:
            message = request.form["message"]
            user_id = c.execute("SELECT users.id FROM users WHERE users.username=?",(name,)).fetchone()[0]
            post_new_message = c.execute("INSERT INTO messages(body, user_id) VALUES (?,?)",(message, user_id))
            username_post = c.execute("SELECT username from users WHERE id=?", (user_id,)).fetchone()[0]
            tup = (username_post, message)
            return json.dumps(tup)

    

if __name__ == '__main__':
    app.run()