from flask import Blueprint, current_app, render_template

blueprint = Blueprint("home", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    current_app.logger.debug("Home route called")
    return render_template("home/index.html", page_name="Home")


@blueprint.route("/about")
def about():
    current_app.logger.debug("About route called")
    return render_template("home/about.html", page_name="About")


@blueprint.route("/settings")
def settings():
    current_app.logger.debug("Settings route called")
    return render_template("home/settings.html", page_name="Settings")
