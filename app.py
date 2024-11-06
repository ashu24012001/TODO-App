from flask import Flask, render_template, request, redirect, url_for #imports Flask and render_template class from flask module
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #Flask constructor takes __name__ as argument which is name of the module(__main__ is module name if it isn't imported as a module in another script).
# It helps Flask to determine location of Application so that it can find template and static files.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #path to sqlite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #DB Creation

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/') #route decorator that tells Flask which URL should trigger the index()
def index(): #view function to handle requests to the root URL
    todo_list = Todo.query.all()
    # print(todo_list)
    # flask uses jinja template engine to pass and access data. {{}} is used to access each data item in the data set.
    return render_template('base.html', todo_list=todo_list) #Flask will render base.html file which should be located inside templates directory

#POST request done in base.html file is handled below and then home page is rendered.
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo) #delete todo from session
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context(): #As of Flask-SQLAlchemy 3.0, access to db.engine, db.session requires an active flask application context and db.create_all utilizes db.engine, so it requires app context.
        db.create_all() #creates all tables in DB if they don't exist already.
        # new_todo = Todo(title="Todo 1", complete=False)
        # db.session.add(new_todo) #add new todo to session
        # db.session.commit() #commit the changes to DB
    app.run()

'''There are 2 ways to start development server in flask:

1) In terminal, type:
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

2) if __name__ == "__main__"
       app.run(debug=True)
In terminal, type:
python3 app.py'''

#pip install Flask-SQLAlchemy enables users to work easily with SQL DB