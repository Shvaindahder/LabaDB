from flask import session, render_template, redirect, url_for

from app.auth import bp
from app.auth.forms import AuthUser
from connection import connection


def superuser_required(view):
    if not session["is_staff"]:
        return redirect(url_for("main.main"))
    view()


@bp.route("/register_superuser", methods=["GET", "POST"])
def register_superuser():
    form = AuthUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        sql_query = f"INSERT INTO _user VALUES('{username}', '{password}', TRUE)"
        connection.execute(sql_query)
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = AuthUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        sql_query = f"SELECT * FROM _user WHERE username='{username}' AND password='{password}'"

        user = connection.execute(sql_query).fetchone()
        if not user:
            print("Incorrect username or password")
        else:
            session["user"] = {
                "username": username,
                "is_stuff": user[2],
                "is_dep": user[3]
            }
            return redirect(url_for("main.main"))
    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("main.main"))