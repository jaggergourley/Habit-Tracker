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
    completions = db.relationship('Completion', backref='habit', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'completions': [completion.to_dict() for completion in self.completions]
        }

    def __repr__(self):
        return '<Habit %r>' % self.name


class Completion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_completed = db.Column(db.Date, default=datetime.utcnow().date())
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

@app.route('/api/habits', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([habit.to_dict() for habit in habits])

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

@app.route('/delete-habit/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    # Find the habit to delete by its ID
    habit_to_delete = Habit.query.get_or_404(habit_id)

    # Delete the habit from the database
    db.session.delete(habit_to_delete)
    db.session.commit()

    # Redirect back to the homepage or any other appropriate page
    return redirect(url_for('index'))

@app.route('/complete-habit/<int:habit_id>', methods=['POST'])
def complete_habit(habit_id):
    # Find the habit to mark as completed by its ID
    habit = Habit.query.get_or_404(habit_id)
    
    # Check if there's already a completion for today
    today = datetime.utcnow().date()
    existing_completion = Completion.query.filter_by(habit_id=habit.id).filter(db.func.date(Completion.date_completed) == today).first()

    if not existing_completion:
        completion = Completion(habit_id=habit.id)
        db.session.add(completion)
        db.session.commit()

    # Redirect back to the homepage
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)