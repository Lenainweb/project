from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in', default = False)
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    password_again= PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')


class AddAdminForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Add')


class AddProductForm(FlaskForm):
    name_of_product = StringField('Product', validators=[InputRequired()])
    size = StringField('Size', validators=[InputRequired()])
    cost = StringField('Cost', validators=[InputRequired()])
    product_description = TextAreaField('Description', validators=[InputRequired()])
    file = FileField('Images')
    submit = SubmitField('Add')


class DelProductForm(FlaskForm):
    name_of_product = StringField('Product', validators=[InputRequired()])
    size = StringField('Size', validators=[InputRequired()])
    submit = SubmitField('Delete')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password')
    new_password = PasswordField('New password')
    new_password2 = PasswordField('Confirm new password')
    submit = SubmitField('Update password')

class UserAccountForm(FlaskForm):
    first_name = StringField('First name',  validators=[InputRequired()])
    last_name = StringField('Last name', validators=[InputRequired()])
    email = EmailField('Email', validators=[Length(1, 64), Email()])
    submit = SubmitField('Save change')


class ContactUsForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[Length(1, 64), Email()])
    subject = StringField('Subject', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')


class AddressForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    company_name = StringField('Company Name')
    email = EmailField('Email', validators=[Length(1, 64), Email()])
    phone = StringField('Phone', validators=[InputRequired()])
    street = StringField('Street', validators=[InputRequired()])
    apartment = StringField('Apartment', validators=[InputRequired()])
    town = StringField('Town', validators=[InputRequired()])
    state = StringField('State', validators=[InputRequired()])
    zips = StringField('Zip', validators=[InputRequired()])
    submit = SubmitField('Save Billing Address')


class AddToCartForm(FlaskForm):
    submit = SubmitField('ADD TO CART')


class ConfirmCancelOtherForm(FlaskForm):
    submit = SubmitField('Cancel')
    submit1 = SubmitField('Confirm')