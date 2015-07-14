from flask import render_template, request
from models import Category, Todo, Priority, db
from todoapp import app

@app.route('/')
def list_all():
    return render_template(
            'list.html',
            categories=Category.query.all(),
            todos=Todo.query.join(Priority).order_by(Priority.value.desc())
    )


# respond to a POST request
@app.route('/new-task', methods=['POST'])
def new():
    if request.method == 'POST':
        category = Category.query.filter_by(id=request.form['category']).first()
        priority = Priority.query.filter_by(id=request.form['priority']).first()
        todo = Task(category, priority, request.form['description'])
        # Write to the DB
        db.session.add(todo)
        db.session.commit()
        # Show all todos
        return redirect('/')
    else:
        # Something went wrong, ask user to create a new todo
        return render_template(
                'new-task.html',
                page='new-task',
                categories = Category.query.all(),
                priorities = Priority.query.all()
        )

@app.route('/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo = Task.query.get(todo_id)
    if request.method == 'GET':
        # Renders template for new-task and insert existing todo
        return render_template(
                'new-task.html',
                todo=todo,
                categories=Category.query.all(),
                priorities=Priority.query.all()
        )
    else:
        # Update the todo
        category = Category.query.filter_by(id=request.form['category']).first()
        priority = Priority.query.filter_by(id=request.form['priority']).first()
        description = request.form['description']
        todo.category = category
        todo.priority = priority
        todo.description = description
        db.session.commit()
        return redirect('/')

