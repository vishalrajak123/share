import datetime
from flask import Flask,render_template,request,sessions,session
app= Flask(__name__)
notes=['asdad','dasdsa']
@app.route("/",methods=["GET","POST"])
def index():
    if request.method =="POST":
        note = request.form.get("note")
        notes.append(note)
    return render_template("index.html", notes=notes)


@app.route("/sougata")
def sougata():
    head="soudsfsffds"
    now =datetime.datetime.now()
    return render_template("index1.html",head=now)
@app.route("/form" , methods=["GET","POST"])
def form():
    if request.method=="GET":
        return ("use the form")
    else:
        name=request.form.get("name")
        return render_template("index2.html",name=name        )


app.run(debug=True)