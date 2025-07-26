from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterForm(LoginForm):
    username = StringField('Username', validators=[DataRequired()])

class AddBookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    submit = SubmitField('Lookup & Add')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')

class ChallengeForm(FlaskForm):
    target = IntegerField('Books to read', validators=[DataRequired()])
    submit = SubmitField('Set Challenge')
