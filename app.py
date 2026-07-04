from flask import Flask,render_template,request,redirect, url_for
import database
database.create_table()
app = Flask(__name__)
@app.route("/",methods=['GET','POST'])
def home():
    if request.method == "POST":
        topic = request.form['topic']
        database.add_topic(topic,0)
    tp = database.view_topics()
    return render_template("home.html",topics = tp)


@app.route("/delete/<int:id>")
def delete(id):
    database.delete_topic(id)
    return redirect(url_for("home"))    

@app.route("/update/<int:id>",methods=['POST','GET'])
def update(id):
    if request.method == "POST":
        topic = request.form['topic']
        progress = float(request.form["progress"])
        database.update_topic(id,topic,progress)
        return redirect(url_for("home"))
    topic = database.get_topic(id)
    return render_template("update.html", topic=topic)



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login():
    return render_template("login.html")
if __name__ == "__main__":
    app.run(debug=True)
