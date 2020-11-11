from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from application.models import ToDoList



class TodoCheck:
	def __init__(self, message):
		self.message = message

	def __call__(self, form, field):
		todoList = ToDoList.query.all()
		for todo in todoList:
			if todo.task == field.data:
				raise ValidationError(self.message)

class orderedForm(FlaskForm):
    orderedWith = SelectField('Order With',
        choices=[
            ("complete", "Completed"),
            ("id", "Recent"),
            ("old", "Old"),
            ('incomplete', "Incomplete")
        ]
    )
    submit = SubmitField('Order')

class TodoForm(FlaskForm):
	task = StringField('Task',
		validators=[DataRequired(),
		TodoCheck(message='Task already exists')])

	submit = SubmitField('Add Todo')


class updateForm(FlaskForm):
	task = StringField('Task',
		validators=[DataRequired(),
		TodoCheck(message='Task already exists')])

	submit = SubmitField('update Todo')