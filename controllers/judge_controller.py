# controllers/judge_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.score_model import save_score
from models.performer_model import get_active_performers

judge_bp = Blueprint('judge', __name__, url_prefix="/judge")

@judge_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("user") or session["user"]["role"] != "judge":
        return redirect(url_for("auth.login"))

    print(session)

    active_performers = get_active_performers()
    # performer = session.get("performance", 1)
    # Get the performer's voting status
    # performer = get_performer(performance_id)
    # is_voting = performer["is_voting_active"]

    if request.method == "POST":

        performance_id = request.form.get("performance_id")

        scores = {f"Category_{i}": int(request.form.get(f"Category_{i}", 0)) for i in range(1, 6)}
        save_score(f"{performance_id}", session["user"]["user_id"], scores)
        flash("Your vote has been submitted for performer: " + performance_id)

    return render_template("judge.html", judge_name=session["user"]["user_id"], active_performers=active_performers)
