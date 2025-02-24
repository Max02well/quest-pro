from flask import Blueprint, render_template

# Creates a blueprint for main pages (main routes)
main_bp = Blueprint("main_bp", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@main_bp.route("/terms")
def terms():
    return render_template("terms.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")