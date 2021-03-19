from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class addNote(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    content = TextAreaField('Content:', validators=[DataRequired()])
    img = StringField('Img:', validators=[DataRequired()])
    submit = SubmitField('Publish')
