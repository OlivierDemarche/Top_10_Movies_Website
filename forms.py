from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# -----------------------------------------------------------------------
# ---------------------------- EDIT FORM --------------------------------
# -----------------------------------------------------------------------
class MyEditForm(FlaskForm):
    rating = StringField(label='Your rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField(label='Your Review', validators=[DataRequired()])
    submit = SubmitField(label="Edit Movie")


# -----------------------------------------------------------------------
# ---------------------------- ADD FORM --------------------------------
# -----------------------------------------------------------------------
class MyAddingForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")
