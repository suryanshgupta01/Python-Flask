from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from dotenv import load_dotenv
import os
# Load environment variables from the .env file
load_dotenv()
FLASK_RUN_PORT = int(os.getenv('FLASK_RUN_PORT', 5000))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # was not adding any value to the project so deleted it
    # def __repr__(self):
        # return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():    
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        if task_content == '':
            return redirect('/')
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()        
        return render_template('index.html', tasks=tasks)    
    # return render_template('index.html',users=['user1','user2','user3'])

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

# was not adding any value to the project so deleted it
# with app.app_context():
#     db.create_all()
    
if __name__ == '__main__':
    app.run(port=FLASK_RUN_PORT,debug=True)