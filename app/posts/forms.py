from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    photo = FileField('Add a Photo/certificates', validators=[FileAllowed(['jpeg','jpg', 'png', 'pdf', 'docx'])])
    submit = SubmitField('submit')

class LostItemForm(FlaskForm):
    title = StringField("Item Title", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    contact = StringField("Contact Info", validators=[DataRequired()])
    image_file = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Report Lost Item")
