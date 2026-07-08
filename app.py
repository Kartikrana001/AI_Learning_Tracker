from flask import Flask,render_template,request,redirect, url_for,flash
from flask_login import LoginManager,UserMixin,login_user,login_required
import database
database.create_table()
database.user_login()
app = Flask(__name__)
app.secret_key = "learning_tracker_secret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self,id,name,email):
        self.id = id
        self.name = name
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    data = database.get_user_by_id(user_id)
    if data:
        return User(data[0],data[1],data[2])
    return None
@app.route("/", methods=["GET", "POST"])
@login_required
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
@login_required
def delete(id):
    database.delete_topic(id)
    flash("Topic deleted successfully!","danger")
    return redirect(url_for("home"))    

@app.route("/update/<int:id>",methods=['POST','GET'])
@login_required
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
@login_required
def about():
    return render_template("about.html")


@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email'].strip()
        password = request.form['password']
        data = database.email_login(email,password)
        if data:
            current_user = User(data[0],data[1],data[2])
            login_user(current_user)
            flash("Login Successful!", "success")
            return redirect(url_for("home"))
        flash("Incorrect email or password!","danger")
    return render_template("login.html")
@app.route("/signup",methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if any(ch.isdigit() for ch in name) or name == "":
            flash("Invalid user name!","danger")
        elif "@" not in email:
            flash("Invalid email!","danger")
        elif database.email_exists(email):
            flash("User already exists!","danger")
        elif len(password) <8:
            flash("Password must be greater then 8 digit!","danger")
        elif confirm_password != password:
            flash("Password and Confirm password don't matched!","danger")
        else:
            database.add_user(name,email,password)
            flash("Account created successfuly","success")
            return render_template("login.html")
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
