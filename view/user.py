from flask import request, render_template, flash, redirect, url_for
from datetime import datetime
from models import User, Task, task_user
from settings import app, db, bcrypt
from forms import RegistrationForm, LoginForm, CalculationForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/home")
def home():
    return render_template("home.html", title="Home")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created!Please login', "success")
        return redirect(url_for("login"))

    return render_template("registration.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
            flash("You have been logged in!", "success")
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
def account():
    user = User.query.filter_by(id=current_user.id).first()
    average_time = user.time / user.tasks.count()
    return render_template("account.html", title="Account", average_time=average_time)

@app.route("/rating")
def rating():
    users = User.query.all()
    rating = {user.username: user.time/user.tasks.count() for user in users}
    sorted_rating = sorted(rating.items(), key=lambda x: x[1])
    print(sorted_rating)
    return render_template("rating.html", title="Rating", sorted_rating=sorted_rating)

@app.route("/tasks")
def tasks():
    user = User.query.filter_by(id=current_user.id).first()
    current_task_list = [task.id for task in user.tasks]
    tasks = [task.serialize() for task in Task.query.all()]
    return render_template("tasks.html", title="Tasks", tasks=tasks, list =current_task_list)

start = datetime.now()

@app.route("/tasks/<int:task_id>", methods=["GET", "POST", "PATCH"])
def task(task_id):

    task = Task.query.get(task_id).serialize()
    calculation = CalculationForm()
    user = User.query.filter_by(id=current_user.id).first()
    t = Task.query.filter_by(id=task_id).first()
    if calculation.validate_on_submit():
        # user.tasks.append(t)
        # db.session.add(user)
        # db.session.commit()
        if task["result"] == calculation.result.data:
            finish = datetime.now()
            timedelta = finish - user.last_start
            seconds = timedelta.days * 24 * 3600 + timedelta.seconds + user.time
            db.session.query(User).filter_by(id=current_user.id).update(
                dict(time=seconds))
            db.session.commit()
            print(user.time)
            return redirect(url_for("home"))
        else:
            return redirect(url_for("account"))
    db.session.query(User).filter_by(id=current_user.id).update(dict(last_start=datetime.now()))
    db.session.commit()
    return render_template("task.html", title="Task", task=task, calculation=calculation)


if __name__=="__main__":
    app.run(debug=True)
