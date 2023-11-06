from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habits.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)

    def completion_count(self):
        return len(self.completions)


class HabitCompletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    habit = db.relationship("Habit", back_populates="completions")


Habit.completions = db.relationship(
    "HabitCompletion", order_by=HabitCompletion.date, back_populates="habit"
)


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


@app.route("/checkoff/<int:habit_id>")
def checkoff(habit_id):
    habit_completion = HabitCompletion(date=date.today(), habit_id=habit_id)
    db.session.add(habit_completion)
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
