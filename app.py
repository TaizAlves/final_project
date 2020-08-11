import sqlite3
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from utils import login_required, usd



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
        
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        #print(products)
        
        nr = len(products)
    
    
        return render_template("index.html", products = products, nr = nr)

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
            
            # Query database for username  // return as tuples
            cur.execute("SELECT * FROM users WHERE email = (?)", email)
            
            if not request.form['email'] :
                flash("Invalid email")

            for rows in cur:
                #print(rows[2])
                #print(request.form['email'])
                # Ensure username exists and password is correct
                if not check_password_hash(rows[3], request.form['password']):
                    flash("must provide a valid email/password")
                    return render_template("login.html")
           
                # Remember which user has logged in
                
                session["user_id"] = rows[0]
                flash("login susscessfully")
                return redirect("/")
                
            
            flash("must provide a valid email/password")
            return render_template("login.html")
              

            # Redirect user to home page
            

        except Exception as e:
            print(e)
            return redirect("/login")
        

    # User reached route via GET 
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/recipes-add", methods=["GET", "POST"])
@login_required
def recipes():
    """Recipies"""
    try:
        if request.method == "GET":
            cur.execute("SELECT name, id  FROM category ORDER BY name")
            
            category = []
            for cat in cur:
                category.append(cat)
            
            #print(category)
            return render_template("recipes/recipes.html", category = category)

        else:

            user_id = session["user_id"]
            title = request.form['title']
            description = request.form['description']
            more_info = request.form['more_info']
            category_id = request.form['category']

            cur.execute("INSERT INTO recipes (title, description, more_info, user_id, category_id) VALUES (?,?,?,?,?)", (title, description, more_info,user_id, category_id)) 
            con.commit()
            
            
            flash("Thank you! New recipe add.")
            return redirect("/recipes", category_id)

    except Exception as e:
            print(e)
            return redirect("/recipes")

@app.route("/recipes/<int:id>")
def show(id):
    try:
        #user_id = [session["user_id"]]
        #print(user_id)

        #colocar como objeto no select !importante!!
        id = [id]
        cur.execute("SELECT recipes.title, recipes.description, recipes.more_info, recipes.created_at, users.name as user_name, recipes.category_id, category.id FROM recipes LEFT JOIN category ON recipes.category_id = category_id LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = (?) GROUP BY recipes.id", id)

        recipe =cur.fetchall()
        
        #print(recipe)

        return render_template("recipes/show.html", recipe = recipe)


    except Exception as error:
        print(error)
        return redirect("/recipes")

@app.route("/recipes")
def allrecipes():
    try:
        #colocar como objeto no select !importante!!
        #user_id = [session["user_id"]]
        #print(user_id)
        
        cur.execute("SELECT users.name as author , recipes.id as recipe_id,recipes.title, recipes.description, recipes.more_info, recipes.created_at, recipes.user_id, recipes.category_id  as category_name FROM recipes LEFT JOIN category ON recipes.category_id = category_id LEFT JOIN users ON users.id == recipes.user_id GROUP BY recipes.title")
        recipes = cur.fetchall()
        print(recipes[0][7])
        
        return render_template("recipes/index.html", recipes = recipes, nr= len(recipes) )


    except Exception as error:
        print(error)
        return redirect(url_for("index"))

@app.route("/add-product", methods=["GET", "POST"])
@login_required
def product():
    """Recipies"""
    try:
        if request.method == "GET":
            user_id = [session["user_id"]]
            cur.execute("SELECT status FROM users WHERE id =(?)", user_id)
            status = cur.fetchall()
            
            status = status[0][0]
            
            
            #print(status)
            if status != "company":
                flash("SORRY! INTERNAL ACCESS ONLY")
                return redirect("/")
            else:

                cur.execute("SELECT name, id  FROM category ORDER BY name")
                
                category = cur.fetchall()      
                
                #print(category)
                return render_template("product/product.html", category = category, status= status)

        else:
            
            user_id = session["user_id"]
            title = request.form['title']
            description = request.form['description']
            price = request.form['price']
            avatar_url = request.form['avatar_url']
            category_id = request.form['category']

            cur.execute("INSERT INTO products (img,title, description,price, user_id, category_id) VALUES (?,?,?,?,?,?)", (avatar_url, title, description,price, user_id, category_id)) 
            con.commit()
            
            
            flash("Thank you! New product add.")
            return redirect("/")
            

    except Exception as error:
        print(error)
        return redirect(url_for("index"))


@app.route("/products")
def allproducts():
    try:
        #colocar como objeto no select !importante!!
        #user_id = [session["user_id"]]
        #print(user_id)
        
                
        cur.execute("SELECT products.img, products.title, products.description, products.price, products.category_id, products.id FROM products LEFT JOIN category ON products.category_id = category_id GROUP BY products.id")
        products = cur.fetchall()
        #print(products)
        
        
        return render_template("product/index.html", products = products, nr= len(products) )


    except Exception as error:
        print(error)
        return redirect(url_for("index"))



@app.route("/products/<int:id>")
def oneProduct(id):
    """Buy products"""

    try:
        
        id = [id]
        cur.execute("SELECT * FROM products WHERE id =(?)", id)

        product =cur.fetchall()

                
        return render_template("product/show.html", product= product, quantity= product[0][7])
        

    except Exception as error:
        print(error)
        return redirect("/products")

@app.route("/products/<int:id>", methods=["POST"])
@login_required
def buy(id):
    """Buy products"""

    try:        
        ## check for the quantity total
        productid = [id]
        cur.execute("SELECT products.quantity FROM products WHERE id = (?)", productid)
        tot = cur.fetchall()
        total = tot[0][0]
        print(total)

        # UPDATE quantity
        updated_quantity = total - int(request.form['quantity'])
        
        cur.execute("UPDATE products SET quantity = (?) WHERE id =(?)", (updated_quantity,id))

        

        user_id = session["user_id"]
        product_id = request.form['product_id']
        quantity= request.form['quantity']
        cur.execute("INSERT INTO sales (user_id, product_id, quantity) VALUES(?,?,?)",( user_id,product_id , quantity))
        con.commit()
        flash("Bought!")

        return redirect("/products/cart")

    except Exception as error:
        print(error)
        return redirect("/products")

@app.route("/products/cart")
@login_required
def cart():
    try:
        #colocar como objeto no select !importante!!
        user_id = [session["user_id"]]
        #print(user_id)
        
        cur.execute("SELECT products.img,products.title, products.price,sales.quantity,sales.created_at,users.status , products.id as productId FROM sales JOIN products ON products.id = sales.product_id JOIN users ON sales.user_id = users.id WHERE products.id = sales.product_id AND users.id = (?)", user_id)
        cart_client= cur.fetchall()
        if not cart_client:
            flash("You have 0 products in your cart")
            return redirect("/products")

        
        cur.execute("SELECT status FROM users WHERE id = (?)", user_id)
        status = cur.fetchall()
        status = status[0][0] 

        if status == "companny":
            return redirect("/sales")

        else:
            
            return render_template("product/cart.html", cart_client = cart_client, nr = len(cart_client) )

        

    except Exception as error:
        print(error)
        return redirect("/products")

@app.route("/sales")
@login_required
def sales():
    try:       

        cur.execute("SELECT products.id,products.title, products.price,sales.quantity,sales.created_at, users.name, users.email, users.status FROM sales JOIN products ON products.id = sales.product_id JOIN users ON sales.user_id = users.id WHERE products.id = sales.product_id ")
        sales = cur.fetchall()
        
        
        user_id = [session["user_id"]]
        cur.execute("SELECT status FROM users WHERE id = (?)", user_id)
        status = cur.fetchall()
        status = status[0][0] 
        

        if status == "company":
            return render_template("product/sales.html", sales = sales, nrs = len(sales))

        else:
            
            return redirect("/products/cart")        

    except Exception as error:
        print(error)
        return redirect("/products")


@app.route("/products/search", methods=["GET", "POST"])
def search():
    """Recipies"""
    try:
        if request.method == "GET":
            
            return redirect('/recipes')
            
            

        else:
            
            
            filter = request.form['filter']
            filter = [filter]
              

            cur.execute("SELECT * FROM products WHERE title OR description LIKE '%'||?||'%'", filter)
            filtered_product= cur.fetchall()
            print(filtered_product)
            
            cur.execute("SELECT * FROM recipes WHERE title OR description LIKE '%'||?||'%'", filter)
            filtered_recipe = cur.fetchall()
            print(filtered_recipe)

            total = len(filtered_product) + len(filtered_recipe)
        
            return render_template("search.html", products = filtered_product, recipe = filtered_recipe, total = total, len_prod = len(filtered_product), len_rec = len(filtered_recipe), filter= filter)

    except Exception as error:
        print(error)
        return redirect("/")