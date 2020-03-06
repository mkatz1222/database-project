from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from RealestateSite.models import User


agentCities = [('any', 'All'), (1, 'Washington'), (2, 'Springfield'), (3, 'Franklin'), (4, 'Lebanon'),
                                        (5, 'Clinton'), (6, 'Greenville'), (7, 'Bristol'),(8, 'Fairview'), (9, 'Salem'),
                                        (10, 'Madison'), (11, 'Georgetown'), (12, 'Arlington'), (13, 'Ashland'),
                                        (14, 'Dover'), (15, 'Oxford'), (16, 'Jackson'), (17, 'Burlington'),
                                        (18, 'Manchester'), (19, 'Milton'), (20, 'Newport')]

houseCities = [('any', 'All'), ('Washington', 'Washington'), ('Springfield', 'Springfield'), ('Franklin', 'Franklin'), ('Lebanon', 'Lebanon'),
                                        ('Clinton', 'Clinton'), ('Greenville', 'Greenville'), ('Bristol', 'Bristol'),('Fairview', 'Fairview'), ('Salem', 'Salem'),
                                        ('Madison', 'Madison'), ('Georgetown', 'Georgetown'), ('Arlington', 'Arlington'), ('Ashland', 'Ashland'),
                                        ('Dover', 'Dover'), ('Oxford', 'Oxford'), ('Jackson', 'Jackson'), ('Burlington', 'Burlington'),
                                        ('Manchester', 'Manchester'), ('Milton', 'Milton'), ('Newport', 'Newport')]

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LogInForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember My Login")
    submit = SubmitField("Login")


class SearchAgentsForm(FlaskForm):
    agentBranch = SelectField("Select Branch", choices=agentCities)
    submit = SubmitField("Search")


class SearchHousesForm(FlaskForm):
    address = StringField("Address")
    price = SelectField("Price Range", choices=[('any', 'Any'), (100000, 'Below $100,000'),
                                                (150000, 'Below $150,000'),
                                                (200000, 'Below $200,000'),(250000, 'Below $250,000'),
                                                (300000, 'Below $300,000'),(350000, 'Below $350,000'),
                                                (400000, 'Below $400,000'),(450000, 'Below $450,000'),
                                                (500000, 'Below $500,000'),(500000, 'Above $500,000')],
                                                validators=[DataRequired()])
    bedrooms = SelectField("Number of Bedrooms", choices=[('any', 'Any'), (0,'0'), (1,'1'), (2,'2'), (3,'3'),
                                                          (4,'4'), (5,'5'), (6,'6'), (7,'7'),
                                                          (8,'8'), (9,'9'), (10,'10'), (11,'11'), (12,'12')])
    bathrooms = SelectField("Number of Bathrooms", choices=[('any', 'Any'), (0,'0'), (1,'1'), (2,'2'), (3,'3'),
                                                          (4,'4'), (5,'5'), (6,'6'), (7,'7'),
                                                          (8,'8'), (9,'9'), (10,'10'), (11,'11'), (12,'12')])
    size = SelectField("Square Feet", choices=[('any', 'Any'), (1000, 'Less than 1000'), (1500, '1500'),
                                               (2000, '2000'),
                                               (2500, '2500'),
                                               (3000, '3000'),
                                               (3500, '3500'),
                                               (4000, '4000')])
    city = SelectField("City", choices=houseCities)
    fence = SelectField("Fenced", choices=[('any', 'Any'), (0, 'No'), (1, "Yes")])
    pool = SelectField("Pool", choices=[('any', 'Any'), (0, 'No'), (1, "Yes")])
    submit = SubmitField("Search")

class PostHouseForm(FlaskForm):
    price = IntegerField("Price", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    bedrooms = SelectField("Number of Bedrooms", choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'),
                                                          (4, '4'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
                                                          (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')],
                                                          validators=[DataRequired()])
    bathrooms = SelectField("Number of Bathrooms", choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'),
                                                            (4, '4'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
                                                            (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')],
                                                            validators=[DataRequired()])
    size = IntegerField("Square Feet",  validators=[DataRequired()])
    city = SelectField("City", choices=houseCities, validators=[DataRequired()])
    age = IntegerField("Age of House", validators=[DataRequired()])
    fence = SelectField("Fenced", choices=[(0, 'No'), (1, "Yes")], validators=[DataRequired()])
    pool = SelectField("Pool", choices=[(0, 'No'), (1, "Yes")], validators=[DataRequired()])
    submit = SubmitField("Submit")


class editAccountForm(FlaskForm):
    buyerName = StringField("Name")
    phoneNumber = IntegerField("Phone Number")
    budget = IntegerField("Budget")
    lfSqft = IntegerField("Desired House Size")
    lfBedrooms = IntegerField("Desired Number of Bedrooms")
    lfBathrooms = IntegerField("Desired Number of Bathrooms")
    lfCity = StringField("Desired City")
    submit = SubmitField("Submit")

class CompareBranchesForm(FlaskForm):
    branchOne = SelectField("Select First Branch", choices=agentCities)
    branchTwo = SelectField("Select Second Branch", choices=agentCities)
    submit = SubmitField("Submit")

