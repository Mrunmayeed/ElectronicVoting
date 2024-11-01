# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import USERS, JUDGES
from flask_session import Session

app = Flask(__name__)
# app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Route: Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = USERS.get(email)
        if user and user["password"] == password:
            session["user"] = user
            if user["role"] == "admin":
                return redirect(url_for("admin"))
            elif user["role"] == "judge":
                return redirect(url_for("judge"))
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")

# Route: Admin Page
@app.route("/admin", methods=["GET", "POST"])
def admin():
    # print(session.get("user"))
    if not session.get("user") or session["user"]["role"] != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        # Handle starting or ending voting, as well as calculating scores
        action = request.form.get("action")
        if action == "start_performance":
            session["performance"] = session.get("performance", 0) + 1
            session["is_voting"] = False
        elif action == "start_voting":
            session["is_voting"] = True
        elif action == "end_voting":
            session["is_voting"] = False

    # Calculate cumulative scores
    cumulative_scores = calculate_cumulative_scores()

    return render_template("admin.html", performance=session.get("performance", 0), is_voting=session.get("is_voting", False), cumulative_scores=cumulative_scores)

# Route: Judge Page
@app.route("/judge", methods=["GET", "POST"])
def judge():
    if not session.get("user") or session["user"]["role"] != "judge":
        return redirect(url_for("login"))

    performance = session.get("performance", 1)
    is_voting = session.get("is_voting", False)

    if request.method == "POST" and is_voting:
        # Save scores from the judge
        scores = {
            "Category_1": int(request.form.get("Category_1", 0)),
            "Category_2": int(request.form.get("Category_2", 0)),
            "Category_3": int(request.form.get("Category_3", 0)),
            "Category_4": int(request.form.get("Category_4", 0)),
            "Category_5": int(request.form.get("Category_5", 0)),
        }
        session[f"performance_{performance}_judge_scores"] = session.get(f"performance_{performance}_judge_scores", {})
        session[f"performance_{performance}_judge_scores"][session["user"]["username"]] = scores
        flash("Your vote has been submitted.")

    return render_template("judge.html", judge_name=session["user"]["username"], performance=performance, is_voting=is_voting)

# Calculate cumulative scores function
def calculate_cumulative_scores():
    performance = session.get("performance", 1)
    cumulative_scores = {f"Category_{i}": 0 for i in range(1, 6)}

    # Retrieve stored votes
    judge_scores = session.get(f"performance_{performance}_judge_scores", {})

    for judge, scores in judge_scores.items():
        weight = 2 if judge == "judge1" else 1
        for category, score in scores.items():
            cumulative_scores[category] += score * weight

    return cumulative_scores

# Route: Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
