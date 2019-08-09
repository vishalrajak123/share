import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name=request.form.get("name")
    class1=request.form.get("class1")
    if not class1 or not name:
        return render_template("error.html", message="wrong")
    file=open("survey.csv","a")
    writer=csv.writer(file)
    writer.writerow((request.form.get("name"),request.form.get("class1")))
    file.close()
    return redirect("/sheet")
   # return render_template("success.html", message="success")
@app.route("/sheet", methods=["GET"])
def get_sheet():
    file=open("survey.csv","r")
    reader=csv.reader(file)
    students=list(reader)
    file.close()
    return render_template("registered.html",students=students)
   # return render_template("error.html", message="success")
