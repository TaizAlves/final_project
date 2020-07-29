import sqlite3
from flask import Flask, render_template, request, redirect, flash
from flask_session import Session

# Configure application
app = Flask(__name__)
app.secret_key = 'flash message'


con = sqlite3.connect('healings.db', check_same_thread=False)
cur = con.cursor()

@app.route("/")
def index():
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS 'users' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        'name' text NOT NULL,
        'email' text UNIQUE NOT NULL,
        'created_at' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP );
    
    CREATE TABLE IF NOT EXISTS 'advisors' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        'name' varchar(255) NOT NULL,
        'email' text UNIQUE NOT NULL,
        'created_at' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
        );

    CREATE TABLE IF NOT EXISTS 'category' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        'name' varchar(255) NOT NULL
        );

    CREATE TABLE IF NOT EXISTS 'recipes' (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        'title' varchar(255) NOT NULL,
        'description' text NOT NULL,
        'more_info' text,
        'created_at' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,
        'advisor_id' INTEGER NOT NULL,
        'category_id' INTEGER NOT NULL,
        'user_id' INTEGER NOT NULL,
        FOREIGN KEY (advisor_id) REFERENCES advisors(id) ON DELETE CASCADE ,
        FOREIGN KEY (category_id) REFERENCES category(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    
    return render_template("index.html")
