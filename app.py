from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habits.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        habit_title = request.form.get("habit")
        if habit_title:
            new_habit = Habit(title=habit_title)
            db.session.add(new_habit)
            db.session.commit()
        return redirect(url_for("index"))
    habits = Habit.query.all()
    return render_template("index.html", habits=habits)


@app.route("/complete/<int:id>")
def complete(id):
    habit = Habit.query.get(id)
    habit.complete = not habit.complete
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete(id):
    habit = Habit.query.get(id)
    if habit:
        db.session.delete(habit)
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
