from flask import Blueprint,render_template,request,redirect, url_for,flash,session,current_app
from flask_login import login_user,logout_user,UserMixin,login_required
from werkzeug.security import generate_password_hash,check_password_hash 
import database
from utiles.otp import generate_otp
from utiles.mail import send_otp

auth = Blueprint("auth",__name__)
class User(UserMixin):
    def __init__(self,id,name,email):
        self.id = id
        self.name = name
        self.email = email

@auth.route("/login", methods=['POST','GET'])
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



@auth.route("/signup",methods=["GET", "POST"])
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
            send_otp(current_app.extensions["mail"],current_app.config["MAIL_USERNAME"],email,otp)
            flash("OTP send to your email!","success")
            return redirect(url_for("auth.otp_signup"))
    return render_template("signup.html")


@auth.route("/otp_signup",methods=['GET','POST'])
def otp_signup():

    if "signup_otp" not in session:
        flash("Please sign up first!", "danger")
        return redirect(url_for("auth.signup"))

    if request.method == "POST":
        otp = ""
        for i in range(1, 7):
            otp += request.form.get(f"otp{i}", "")

        if otp == session.get("signup_otp"):

            if database.email_exists(session["signup_email"]):
                flash("Email already registered!", "danger")
                return redirect(url_for("auth.signup"))

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



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!","success")
    return redirect(url_for("auth.login"))