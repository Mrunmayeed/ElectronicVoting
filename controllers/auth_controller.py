# controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import verify_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = verify_user(email, password)
        if user:
            session["user"] = user
            return redirect(url_for(f"{user['role']}.dashboard"))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
