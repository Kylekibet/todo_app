from wtforms import StringField, SubmitField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf import FlaskForm
from flask_login import current_user
from models import db, Category

class AddTask(FlaskForm):
    task = StringField('Task', validators=[DataRequired()], render_kw={"placeholder": "ADD Task"})
    category_id = SelectField('Category', coerce=int)
    date_due = DateField('Due date', validators=[Optional()])
    add = SubmitField('Add Task')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = db.session.scalars(
            db.select(Category)
            .where(Category.user_id == current_user.id)
            .order_by(Category.name)
        ).all()
        self.category_id.choices = [(0, 'No category')] + [(c.id, c.name) for c in categories]
    
class AddCategory(FlaskForm):
    category = StringField('Category', validators=[DataRequired()], render_kw={"placeholder": "ADD Category"})
    add = SubmitField('Add Category')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "name@example.com"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Log In')
    

class RegisterUser(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "name@example.com"})
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')  