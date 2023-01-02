from wtforms import Form,StringField,PasswordField,IntegerField,SelectField,EmailField,DateField,BooleanField
from wtforms.validators import InputRequired,DataRequired, Length
#class for signup form
class SignupForm(Form):
        exam=[('CAT','Common Aptitude Test'),('GATE','GATE'),('JOB','Job Aptitude'),('OTH','Others')]
        genders=[('MALE',"Male"),('FEMALE','Female'),('OTHERS','Others')]
        courses=[('Btech','Bachelor of Technology'),('BA','Bachelor of Arts'),('BSc','Bachelor of Science'),('BBA','Bachelor of Business Administration'),
        ('MBA','Master of Business Administration'),('MA','Master of Arts'),('MSc','Master of Science'),('MTech','Master of Technology'),('OTH','Others')]
        email_id = EmailField(id='Register_email',validators=[InputRequired(), Length(min=4, max=50)],render_kw={"placeholder": "Let the autofill complete it @gmail.com"})
        password = PasswordField(id='Register_password',validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Type in a password you won't remember"})
        name=StringField(id='Register_name',validators=[InputRequired()],render_kw={"placeholder": "What should we call you?"})
        target=SelectField(id='Register_target',validators=[InputRequired()],choices=exam,render_kw={"placeholder": "What is your aim?"})
        gender=SelectField(id='Register_gender',validators=[InputRequired()],choices=genders,render_kw={"placeholder": "What do you identify as?"})
        college=StringField(id='Register_college',validators=[InputRequired()],render_kw={"placeholder": "Where do you study?"})
        college_location=StringField(id='Register_clg_location',validators=[InputRequired()],render_kw={"placeholder": "Where is your college?"})
        course=SelectField(id='Register_course',validators=[InputRequired()],choices=courses,render_kw={"placeholder": "What Course are you enrolled in?"})
        DOB=DateField(id='Register_DOB',validators=[InputRequired()],render_kw={"placeholder": "Tell us when to wish you?"},format="%Y-%m-%d")
        semester=IntegerField(id='Register_age',validators=[InputRequired()],render_kw={"placeholder": "Which semester are you in? (0 if already passedout) "})
        logincheckbox = BooleanField('login', validators=[DataRequired(), ])
