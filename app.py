from flask import Flask,render_template,request,redirect, url_for,flash
import database
database.create_table()
app = Flask(__name__)
app.secret_key = "learning_tracker_secret"
@app.route("/", methods=["GET", "POST"])
def home():
    search = request.args.get("search")

    if search:
        tp = database.search_topic(search)

        if not tp:
            flash("Topic not found!", "danger")
            tp = database.view_topics()

    else:
        tp = database.view_topics()
    if request.method == "POST":
        topic = request.form["topic"].strip()

        if topic == "":
            flash("Invalid topic!", "danger")

        elif database.topic_exists(topic):
            flash("Topic already exists!", "danger")

        else:
            database.add_topic(topic, 0)
            flash("Topic added successfully!", "success")

        return redirect(url_for("home"))
    return render_template("home.html", topics=tp)


@app.route("/delete/<int:id>")
def delete(id):
    database.delete_topic(id)
    flash("Topic deleted successfully!","danger")
    return redirect(url_for("home"))    

@app.route("/update/<int:id>",methods=['POST','GET'])
def update(id):
    if request.method == "POST":
        topic = request.form['topic'].strip()
        progress = float(request.form["progress"])
        if topic == "":
            flash("Invalid topic!","danger")
        elif progress < 0 or progress > 100:
            flash("Invalid progress!","danger")
        else:
            database.update_topic(id,topic,progress)
            flash("Topic updated successfully!","warning")
        return redirect(url_for("home"))
    topic = database.get_topic(id)
    return render_template("update.html", topic=topic)



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
