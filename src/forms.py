'''
Form definitions for QuickDB application
'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ClientForm(FlaskForm):
    client_name = StringField('Client Name', validators=[DataRequired(), Length(max=100)])
    primary_contact_name = StringField('Primary Contact Name', validators=[Length(max=100)])
    primary_contact_email = StringField('Primary Contact Email', validators=[Optional(), Email(), Length(max=100)])
    primary_contact_phone = StringField('Primary Contact Phone', validators=[Length(max=20)])
    company_address = TextAreaField('Company Address')
    client_status = SelectField('Client Status', choices=[
        ('Prospect', 'Prospect'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ])

class ServiceForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired(), Length(max=100)])
    engagement_date = DateField('Engagement Date', validators=[Optional()], format='%Y-%m-%d')
    service_status = SelectField('Service Status', choices=[
        ('Planned', 'Planned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ])

class NoteForm(FlaskForm):
    note_text = TextAreaField('Note', validators=[DataRequired()])

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[Optional(), Length(min=8)])
    role = SelectField('Role', choices=[
        ('Staff', 'Staff'),
        ('Admin', 'Admin')
    ])
    is_active = BooleanField('Active', default=True)
