from flask import Flask, render_template, redirect, url_for, request
from application import app, db
from application.models import ToDoList
from application.forms import TodoForm, updateForm, orderedForm




@app.route('/', methods = ['GET', 'POST'])
def index():
	form = orderedForm()
	totals = {"total": ToDoList.query.count(), "totalCompleted" : ToDoList.query.filter_by(status=True).count()}
	if form.orderedWith.data == "id":
		todoList = ToDoList.query.order_by(ToDoList.id.desc()).all()
	elif form.orderedWith.data == "complete":
		todoList = ToDoList.query.order_by(ToDoList.status.desc()).all()
	elif form.orderedWith.data == "incomplete":
		todoList = ToDoList.query.order_by(ToDoList.status).all()	
	else:
		todoList = ToDoList.query.all()
	return render_template('index.html', todoList = todoList, form=form, totals=totals)

@app.route('/add', methods=['GET', 'POST'])
def add():
	form = TodoForm()
	if form.validate_on_submit():
		
		new_task= ToDoList(task=form.task.data)
		db.session.add(new_task)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template ('add.html', form=form)



@app.route('/complete/<idNum>')
def complete(idNum):
	task= ToDoList.query.get(idNum)
	task.status= True
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/incomplete/<idNum>')
def incomplete(idNum):
	task= ToDoList.query.get(idNum)
	task.status= False
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/update/<idNum>', methods=['POST', 'GET'])
def update(idNum):
	form = updateForm()
	task= ToDoList.query.get(idNum)
	if form.validate_on_submit():
		task.task=form.task.data
		db.session.commit()
		return redirect(url_for('index'))
	elif request.method == 'GET':
		form.task.data = task.task
	
	return render_template('update.html', title='Update your todo', form=form)

@app.route('/delete/<idNum>')
def delete(idNum):
	task_1= ToDoList.query.get(idNum)
	db.session.delete(task_1)
	db.session.commit()
	return redirect(url_for('index'))

