from flask import Flask, render_template, url_for, request, redirect
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
    # Query all habits
    habits = Habit.query.all()
    
    # Pass them to the template
    return render_template('index.html', habits=habits)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/add-habit', methods=['POST'])
def add_habit():
    # Get data from the form
    name = request.form.get('name')
    description = request.form.get('description')
    
    # Create new Habit object
    new_habit = Habit(name=name, description=description)
    
    # Add to the database
    db.session.add(new_habit)
    db.session.commit()
    
    # Redirect back to the homepage
    return redirect(url_for('index'))