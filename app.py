from flask import Flask,render_template,request,redirect, url_for,flash,session
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash 
from flask_mail import Mail
from dotenv import load_dotenv
import database ,os
from utiles.otp import generate_otp
from utiles.mail import send_otp
from routes.auth import auth

database.create_table()
database.user_login()
load_dotenv()
app = Flask(__name__)
app.secret_key = "learning_tracker_secret"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = None

class User(UserMixin):
    def __init__(self,id,name,email):
        self.id = id
        self.name = name
        self.email = email

app.register_blueprint(auth)

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
    stats = database.get_statistics(current_user.id)
    chart_data = {"completed": stats["completed"],"in_progress": stats["in_progress"],"not_started": stats["not_started"]}
    if search:
        tp = database.search_topic(search,current_user.id)

        if not tp:
            flash("Topic not found!", "danger")
            tp = database.view_topics(current_user.id)
    else:
        tp = database.view_topics(current_user.id)
    if request.method == "POST":
        topic = request.form["topic"].strip()
        category=request.form["category"]
        if topic == "":
            flash("Invalid topic!", "danger")

        elif database.topic_exists(topic,current_user.id):
            flash("Topic already exists!", "danger")

        else:
            database.add_topic(topic, 0,current_user.id,category)
            flash("Topic added successfully!", "success")

        return redirect(url_for("home"))
    return render_template("home.html", topics=tp , stats=stats, chart_data=chart_data )


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    database.delete_topic(id,current_user.id)
    flash("Topic deleted successfully!","danger")
    return redirect(url_for("home"))    

@app.route("/update/<int:id>",methods=['POST','GET'])
@login_required
def update(id):
    if request.method == "POST":
        topic = request.form['topic'].strip()
        progress = float(request.form["progress"])
        category = request.form["category"]

        if topic == "":
            flash("Invalid topic!","danger")
        elif progress < 0 or progress > 100:
            flash("Invalid progress!","danger")
        else:
            database.update_topic(id,topic,progress,current_user.id,category)
            flash("Topic updated successfully!","warning")
        return redirect(url_for("home"))
    topic = database.get_topic(id,current_user.id)
    return render_template("update.html", topic=topic)



@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/forgot_password", methods = ["GET","POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"].strip()
        data =database.get_user_by_email(email)
        if not data:
            flash("Email Not Found!","danger")
            return redirect(url_for("forgot_password"))
        otp = generate_otp()
        session["otp"] = otp
        session["reset_email"] = email.strip()
        session["otp_verified"] = False
        send_otp(mail,app.config['MAIL_USERNAME'],email,otp)
        flash("OTP sent to your email.","success")
        return redirect(url_for("otp_verify"))
    return render_template("forgot_password.html")
@app.route("/otp_verify",methods=["GET","POST"])
def otp_verify():
    if request.method == "POST":
        otp = ""
        for i in range(1, 7):
            otp += request.form.get(f"otp{i}", "")
        if otp == session.get("otp"):
            session["otp_verified"] = True
            session.pop("otp",None)
            flash("OTP Verified Successfully!", "success")
            return redirect(url_for("change_password"))
        else:
            flash("Invalid OTP!", "danger")
    return render_template("otp_verify.html")

@app.route("/change_password",methods= ["GET","POST"])
def change_password():
    if not session.get("otp_verified"):
        flash("Please verify OTP first!", "danger")
        return redirect(url_for("forgot_password"))
    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if len(password) < 8:
            flash("Password must be at least 8 characters!", "danger")
        elif password != confirm_password:
            flash("Password and confirm password do not matched!", "danger")
        else:
            hashed_password = generate_password_hash(password)
            database.update_password(session["reset_email"],hashed_password)
            session.pop("otp_verified", None)
            session.pop("reset_email", None)
            flash("Password changed successfully!", "success")
            return redirect(url_for("auth.login"))
    return render_template("change_password.html")

if __name__ == "__main__":
    app.run(debug=True)
