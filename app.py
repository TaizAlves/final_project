import sqlite3
from flask import Flask, render_template, request, redirect, flash, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from utils import login_required



# Configure application
app = Flask(__name__)
app.secret_key = 'flash message'


con = sqlite3.connect('healings.db', check_same_thread=False)
cur = con.cursor()


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    try:
        cur.executescript('''
       

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
            'category_id' INTEGER NOT NULL,
            'user_id' INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES category(id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        ''')

        cur.execute("SELECT * FROM recipes")
        rows = cur.fetchall()
        
    
        return render_template("index.html", rows = rows)

    except Exception as e:
        print(e)
        return e


@app.route("/register", methods = ["GET", "POST"])
def register():
    
    if request.method == "GET":
        return render_template("register.html") 
    else:
        try:
            name = request.form['username']
            if not name:
                return flash("name not valid")

            email = request.form['email']
            if not email:
                return flash("must privide  a valid  email")

            password = request.form['password']
            rePassword = request.form['rePassword']
                     
            if not password or rePassword != password :
                return flash("password and confirmation must math")
            
            status = request.form['status']
            # hash the password 
            hash = generate_password_hash(request.form['password'])

            cur.executescript('''
                CREATE TABLE IF NOT EXISTS 'users' (
                    'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    'name' text NOT NULL,
                    'email' text UNIQUE NOT NULL,
                    'hash' text NOT NULL,
                    'status', text NOT NULL DEFAULT "client",
                    'created_at' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP );
                    ''')
            
            try: 
                cur.execute("INSERT INTO users (name, email, hash, status) VALUES (?,?,?, ?)", (name, email, hash, status))
                con.commit()
            except :
                flash("Error upload the info into the database")
                return redirect("/register")
                
            
            if not email :
                return flash("Email already exists")

            
            # Display a flash message
            flash("Registered!")
            
       
            return redirect("/")

        except Exception as e:
            print(e)
            return redirect("/register")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        try:
            # Ensure username was submitted
            if not request.form['email']:
                flash("must provide email")

            # Ensure password was submitted
            elif not request.form['password']:
                flash("must provide password")
            
            #tem que colocar como objeto 
            email = [request.form['email']]
            print(email)

            # Query database for username  // return as tuples
            cur.execute("SELECT * FROM users WHERE email = (?)", email)

            if not email:
                flash("Invalid email")
            for rows in cur:
                print(rows)
                # Ensure username exists and password is correct
                if not rows or not check_password_hash(rows[2], request.form["password"]):
                    flash("must provide password")

                # Remember which user has logged in
                session["user_id"] = rows[0]

            # Redirect user to home page
            return redirect("/")

        except Exception as e:
            print(e)
            return redirect("/login")
        

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/recipes", methods=["GET", "POST"])
@login_required
def recipes():
    """Recipies"""
    try:
        if request.method == "GET":
            cur.execute("SELECT name FROM category")
            
            category = []
            for cat in cur:
                print(cat)
                category.append(cat)
            
            print(category)
            return render_template("recipes.html", category = category)

        else:
            return redirect("/")
    except Exception as e:
            print(e)
            return redirect("/recipes")
