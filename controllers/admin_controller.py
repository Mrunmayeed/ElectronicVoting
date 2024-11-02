# controllers/admin_controller.py
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from utils.score_utils import calculate_cumulative_scores
from models.performer_model import create_performer, update_voting_status, update_cumulative_scores, get_performer

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")

@admin_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    print(session)
    if not session.get("user") or session["user"]["role"] != "admin":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        action = request.form.get("action")
        performance_id = request.form.get("performance_id")

        if not performance_id:
            flash("Please enter a performance ID.")
            return redirect(url_for("admin.dashboard"))


        if action == "start_performance":
            # session["performance"] = request.form.get("performer")
            session["performance"] = create_performer(performance_id)

        elif action == "start_voting":
            session["performance"] = get_performer(performance_id)
            update_voting_status(session['performance']['performance_id'], True)
            session["performance"]["is_voting_active"] = True

        elif action == "end_voting":
            session["performance"] = get_performer(performance_id)
            update_voting_status(session['performance']['performance_id'], False)
            session["performance"]["is_voting_active"] = False
            cumulative_scores = calculate_cumulative_scores(session['performance']['performance_id'])
            session["performance"]["cumulative_scores"]=cumulative_scores
            update_cumulative_scores(performance_id, cumulative_scores)
            flash("Voting ended.")


    return render_template("admin.html", performer=session.get("performance",0))