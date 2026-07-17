from flask import Flask,render_template,request,redirect, url_for,flash,session
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash 
from flask_mail import Mail, Message
from dotenv import load_dotenv
import database,os
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
login_manager.login_view = "login"
login_manager.login_message = None

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
        tp = database.search_topic(search,current_user.id)

        if not tp:
            flash("Topic not found!", "danger")
            tp = database.view_topics(current_user.id)

    else:
        tp = database.view_topics(current_user.id)
    if request.method == "POST":
        topic = request.form["topic"].strip()

        if topic == "":
            flash("Invalid topic!", "danger")

        elif database.topic_exists(topic,current_user.id):
            flash("Topic already exists!", "danger")

        else:
            database.add_topic(topic, 0,current_user.id)
            flash("Topic added successfully!", "success")

        return redirect(url_for("home"))
    return render_template("home.html", topics=tp)


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
        if topic == "":
            flash("Invalid topic!","danger")
        elif progress < 0 or progress > 100:
            flash("Invalid progress!","danger")
        else:
            database.update_topic(id,topic,progress,current_user.id)
            flash("Topic updated successfully!","warning")
        return redirect(url_for("home"))
    topic = database.get_topic(id,current_user.id)
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
        data = database.get_user_by_email(email)
        if data and check_password_hash(data[3],password):
            user = User(data[0],data[1],data[2])
            login_user(user)
            flash("Login Successful!", "success")
            return redirect(url_for("home"))
        flash("Incorrect email or password!","danger")
    return render_template("login.html")

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
        session["reset_email"] = email
        session["otp_verified"] = False
        print(email)
        print(otp)
        send_otp(email,otp)
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
    return render_template("change_password.html")
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
        elif len(password) < 8:
            flash("Password must be at least 8 characters!","danger")
        elif confirm_password != password:
            flash("Password and Confirm password don't matched!","danger")
        else:
            session['signup_name'] = name
            session['signup_email'] = email
            session['signup_password'] = generate_password_hash(password)
            otp = generate_otp()
            session["signup_otp"] = otp
            send_otp(email,otp)

            return redirect(url_for("otp_signup"))
    return render_template("signup.html")

@app.route("/otp_signup",methods=['GET','POST'])
def otp_signup():

    if "signup_otp" not in session:
        flash("Please sign up first!", "danger")
        return redirect(url_for("signup"))

    if request.method == "POST":
        otp = ""
        for i in range(1, 7):
            otp += request.form.get(f"otp{i}", "")

        if otp == session.get("signup_otp"):

            if database.email_exists(session["signup_email"]):
                flash("Email already registered!", "danger")
                return redirect(url_for("signup"))

            database.add_user(session["signup_name"],session["signup_email"],session["signup_password"])
            data = database.get_user_by_email(session["signup_email"])
            user = User(data[0], data[1], data[2])
            login_user(user)
            flash("Account created successfully!","success")
            session.pop("signup_otp",None)
            session.pop("signup_name",None)
            session.pop("signup_email",None)
            session.pop("signup_password",None)
            return redirect(url_for("home"))
        else:
            flash("Invalid OTP!", "danger")
    return render_template("otp_signup.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!","success")
    return redirect(url_for("login"))



@app.route("/test_mail")
def test_mail():
    msg = Message(
        subject="Flask Mail Test",
        sender=app.config["MAIL_USERNAME"],
        recipients=[app.config["MAIL_USERNAME"]])
    msg.body = "Congratulations! Flask-Mail is working successfully."
    mail.send(msg)
    return "Email Sent Successfully!"


def generate_otp():
    import random
    return f"{random.randint(0,999999):06d}"

def send_otp(email,otp):
    msg = Message(
        subject="otp from AI_LEARNING_TRACKER",
        sender = app.config["MAIL_USERNAME"],
        recipients= [email]
    )
    msg.body  = f"Your OTP is {otp}"
    mail.send(msg)



if __name__ == "__main__":
    app.run(debug=True)
