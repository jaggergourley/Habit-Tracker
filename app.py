from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to the Completion model
    completions = db.relationship('Completion', backref='habit', lazy=True)

    def __repr__(self):
        return '<Habit %r>' % self.name


class Completion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)

    def __repr__(self):
        return '<Completion for %r on %r>' % (self.habit.name, self.date_completed)



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)