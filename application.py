import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method=="POST":
        if not request.form.get("symbol"):
            return apology("misiing symbol")
        elif not request.form.get("share"):
            return apology("missing share")
        elif not request.form.get("share").isdigit():
            return apology("invalid share")
        symbol=request.form.get("symbol").upper()
        quote=lookup(symbol)
        if  quote==None:
            return apology("invalid symbol")
        cash=db.execute("SELECT cash FROM users where id=:id",id=session["user_id"])
        cash=cash[0]['cash']
        price=(quote["price"])
        share=int(request.form.get("share"))
        updated_cash=cash-(share*price)
        if updated_cash<0:
            return apology("cant afford")
        db.execute("UPDATE users SET cash=:updated_cash where id=:id",updated_cash=updated_cash,id=session["user_id"])
       # rows=db.execute("SELECT * FROM bag WHERE id=:id AND symbol=:symbol",id=session["user_id"],symbol=symbol)
       # if row==0:
       #     db.execute("INSERT INTO bag(id,symbol,share) VALUES(:id,:symbol,:share)",id=session["user_id"],symbol=symbol,share=share )
       # else:
       #     db.execute("UPDATE bag share=share+:share",share=share)


    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


#@app.route("/history")
#@login_required
#def history():
#    """Show history of transactions"""
 #   return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method=="POST":


        if not request.form.get("symbol"):
            return apology("symbol no tfound")
        symbol= request.form.get("symbol").upper()
        quote=lookup(symbol)
        if not quote:
            return apology("invalid")
        return render_template("quoted.html",name=quote["name"],symbol=symbol,price=quote["price"])
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method=="POST":
        if not request.form.get("username"):
            return apology("username not found")
        elif not request.form.get("password"):
            return apology("password not found")
        elif request.form.get("password")!=request.form.get("confirm_password"):
            return apology("password doesnot match")

        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        result=db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash = hash)
        if not result:
            return apology("username taken")

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")
    return apology("TODo")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    """Sell shares of stock"""
    if request.method=='POST':
        if not request.form.get("symbol"):
            return apology("invalid symbol")
        elif not request.form.get("share"):
            return apology("invalid share")
        elif not request.form.get("share").isdigit():
            return apology("invalid share number")
        symbol=request.form.get("symbol").upper()
        quote=lookup(symbol)
        if  quote==None:

            return apology("invalid symbol")
        share=request.form.get("share")
        price=quote["price"][0]
        cash_increase=price*share
        db.execute("UPDATE users SET cash=cash+:cash_increase WHERE id=:id",cash_increase=request.get.form("cash_increase"))
    else:
        return render_template("sell.html")
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
