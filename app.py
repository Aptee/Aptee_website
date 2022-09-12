#importing required packages
from datetime import datetime
import gspread
import flask
from wtforms import Form,StringField,PasswordField,IntegerField,SelectField,EmailField,DateField,BooleanField
from wtforms.validators import InputRequired,DataRequired, Length
import time
import random
from flask_mail import Mail,Message
from cryptography.fernet import Fernet
import string
from keygenerator import generatekey
cipher_suite = Fernet(bytes(generatekey(seed=445),'UTF-8'))
#configuring flask app
app = flask.Flask(__name__, template_folder="Templates")
app.config['SECRET_KEY']='abcdefghijkhlmnop'
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'apteeproject@gmail.com'
app.config['MAIL_PASSWORD'] = str(cipher_suite.decrypt(bytes('gAAAAABivcvM07hd5UvYq-h_Qi3_AXivMrKkhaWqvzzvlQ0PFffl4pk7tF7JpYCvADHYZITI53DDANHAvdheAdCwLR1Lmd2pPYonRE4QrPrCAh_6xUanbGo=','UTF-8')),'UTF-8')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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
#connecting the login sheet to backend
auth =  {
  "type": "service_account",
  "project_id": str(cipher_suite.decrypt(bytes('gAAAAABivv2DfPUWU20sCKtRuHRqWeNUw3fcCOmxHG3m5qOhzCPKrBKl5uq7iiAEfiMSLI_gSDEWEP7tO54s43IcR7xaOjtLWw==','UTF-8')),'UTF-8'),
  "private_key_id": str(cipher_suite.decrypt(bytes('gAAAAABivv9ULkTSsOLABKn3a8XIaij6V1V1JLzOU4C1gocLmDhKwrnIpjfBIFd_PWZ-MCm8mYRxKfDiz1XIRqq50bKgV8qijHabQdIBZG-aFY6fgl6nTxFPx9DowbH08Yub_2lRBEDn','UTF-8')),'UTF-8'),
  "private_key": str(cipher_suite.decrypt(bytes('gAAAAABivv8EirIommtvEVutDKROJA8-3hLDKhHzhDyoUkLunHuTz--_qkrFdgJAF6w8T7KzXQXNWspKR-gSgTnoH_u4NBhJYnkBEzOZfJg-bE9zy_RL8sWcAMnDEpesuB9KHUWAS0m81pNp0DOvN2A3pH9rdOfwume1zR3FoTAboKHi7Qg5zvXsy8b2KTslVptAeSLdsjQv9yaRXs7qXiCRAJVOyN03stgga8RbgTD5iQmOdXfPSRRRMiu5nZ0QriLfyp2NWNsadYOrF-tybA6-07PiliOSpv2dCC1ef64hXFN1r3jbSTGRXvKFKXMofYPZdFnINh9e37JNLnp3EOvwToYmo86ZFxnnTfVP3zpP7ijmJFA6neFJLbgqaTwO7X7Nyel2lOu1utZ069GQ7TovsDSfnsyHFcjwtX_WRAr0nEzciJhOOvgSQIICHnUPMkJAlq0U9qs9UtHWGx7ITZp258sLFiQLd8I9U5AHkN6w1p2LGx7jzlLATXZ-B18HC9f_jyLzqZ-p_1Y2xnAc_ezoCvmablrjAOeThVdrEdVtbxsxZYkILRmX7B506cBOngEhf-9CxEcxIoqj6gL1m2txaxQ8MTCRidcgAkvM7PeUnGtdm2RWI2qOSSJUne9T7ULBV62XtcEDFOyE42MxiEWPBXzWE-kbpMI2vpEsnP22tEr2KjiMcNRNt0k7trhQ-PMMFpVRIGgPhMor7jobxUtKtoxpQZe5H5Q4WJeCpuNRzZZ77B00rj3L7ltdZElUE59AiTMDcpspulBW1A9AXo5mJjHB41dOzVQqkHU6aHUordV1BGFFB3eNIYc2Z7LXhWG3k2m38MRCCnO58Pobj3Cho2c5R6yJluBI_KtnwN7Kb0JiUBMhFAf9qLCgv20hIAjG1Dpjn7Uq4dsy0fCNznd58CAgb5oJIuc58zwtQMCTbXPApokabtzusfOiQKpoLnisFDC0hP4wRXVA4iNs4fY_dxrx1AGqK1nvXezudIz4fpu_5jAj82i7zu1LoWwO70OedmtzoUkwEdqzE4N3sF5bY5wbmAzfegRXpqDzUa2pJNP2fbs5QMPGtCqRHq5WcnLaALBE71ft8bx2A_mt13cPor3bPV1YcQ9y9PKnHRPo1px5QKeCnHnd8Agkw_ULNaV6K4xTSZ8l_8W_Y3NP-JGc_bBJ5pG_bMoeY0N8DJ2u74TIqqnGmVs9gtLmpwLBgUuUb5QwjqTwkNlMhjlV8NL4KrI9pa6fsnd6BvNn7Pt9OGTpsxPgsGroJQEMkOzxtvBDyqajGxoRfvHcayfvtIyHoA907el0gSgoHjiSEFns_bV9v9iI5HWS5WR1ZEeRFEhbhoqjoTjZ7qE48hMdej0WUGx6Il6BX8MMYaZxWbdWi32lG9YTl0odOU32gevRRXUWlx4ES3dCEc6A1f1XSh-9Enaah10LJIerJSCMEt6O9uad8eVzUtIofNbD4ndIMr-I08f5Ulycd7ZhNu7TY-lKsnZIUohJf5JyqhLd6gltDTQhCX2zly6Pjx5cuoY33DFtvmyfr0PjSQgTbV0KKJ8hcd9cm-NT-MS51C3aOqUXyEgY_-9HOyqJq7Oggj8K9rfCNWyZJE603j_KDDYceeLCMhsjweoJy43goI8iWKLkE6Uz-JhnKi7VwScs23k0Y6BuegrHT2sRAsG8gFRmb1BlZU2pTFkkUqkeh2r9BRGyP-cK996jRFDY5O2riC8EbkJyJ1OxidfS26UbQWMFRs8PsujLYYTCQRg6xChIrqi_9GgqKxrPg89vVwEM-1KXlz2R5n7gDnwbZp2HSvm-Rc-nL7xfAWzP-6it7R8EZ1fBJN9eMM3YOacA_pUSUpwk0FlByKODq_Jj_5EZUpjlcJnTi0u8B59cEcd5VUG2huzREt6AJWskNXx5aAPHhbMW1inP5sgFk57ARz52F58Msi36bAwrgBlW64n69NLKLEZX161LHSrvsOLo5Tupap3udQvuXHoNOvoZvAy4dUWKw0g7mKhwICge5CvnckZS8ScajCGIM3hluEgNbjAVVKScpsSvVZu_DpDBZ_sPAwlBRNuUAYLGK-o4_wo8AKo_eJ8oW3VUi7mOOchyd5E-mPdO2jYTn1Zvl9US4yOvv7WF15AZ_yGkaluZFMwSPF2VxFQEUEDqKc-hyPkUgeLbtUe29wKCrogV-BTKCxqbASXUdeyR9HRjke2xQCSEF0yLaqzirqRB6z-ztgcy-0sZNuIImXAn_n5EwFGoQuNV3wKpVRomS-nqoLJMJ5-UXrfJ1K73PHuOpnrbyA0UbAC2LhsIe1OU3NO9Y705xzX4y6MyxiMJODwJqhnR7oLdfAVtu7anhiIWYi1dVrg=','UTF-8')),'UTF-8'),
  "client_email": str(cipher_suite.decrypt(bytes('gAAAAABivv29jL7maeToK2Q0FZSVpMsqMldf9iA5aFWOWyZEpA2arExe6NdZQTigFeobBAf8WuTyw-HAOS6WNPHAvaVvSmy7qWqhcMyDR5jVOmxZNn28LlUR3BDcER7h8HfR0GdYl0Uv','UTF-8')),'UTF-8'),
  "client_id": str(cipher_suite.decrypt(bytes('gAAAAABivv3lfsJ37JJQmCNSzUJn1QpZz6Z74LoYruWIcWAVUWcDm6wi8A6AePUG8PjkVTNV_5z-MNHhwwRnU3IRT-RSBbr-HM2cs3Qmy0u__5u4ywBDW28=','UTF-8')),'UTF-8'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": str(cipher_suite.decrypt(bytes('gAAAAABivv-cbRoolOIBUwguOitM3pdrml17SGKSHJmR5DMODHQWgJoHyb2-rc3-txz2_PVMMcMMPT6AMI6rOZ8n0cer__q1e8_Yq3AxVI0lvKm297F4IjTU1XAL2bnA0Bzri8GTrdkwjWixoAmw-NQhRr13IHCDGzKNINzGbLhCY9LMWvG8kJNw8eMUvELAM1ypz4c6_ywbH6KRTj8x1FqEfpiLBOt49g==','UTF-8')),'UTF-8')
}
def send_email(Header,html,email,param):
        msg = Message(
                        Header,
                        sender ='apteeproject@gmail.com',
                        recipients = [email]
                        )
        msg.html=flask.render_template(html,name=param[0],OTP=param[1],link=param[2])
        mail.send(msg)
gc = gspread.service_account_from_dict(auth)
@app.route('/', methods =['POST', 'GET'])
def home():
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1CyWjl6Y5Gi_e3z7A8wtw-qOaBe3GvCD4sqWWvaMubXY/edit?usp=sharing')
        wks=sh.worksheet("Client_Details")
        wks1=sh.worksheet("Client_Sessions")
        form = SignupForm(flask.request.form)
        Client_ip=flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.environ['REMOTE_ADDR'])
        if form.email_id.data:
                if form.email_id.data in wks.col_values(2):
                        pos =wks.find(form.email_id.data.lower())
                        row =wks.row_values(pos.row)
                        if form.password.data!=row[3]:
                                return flask.render_template('index.html',form=form,message="Password incorrect",alert_colour=1)
                        else:
                                otp=random.randint(10000,99999)
                                pos2=wks1.find(row[0])
                                if pos2:
                                        wks1.batch_update([{"range": "C"+str(pos2.row)+":D"+str(pos2.row), 
                                                                "values" : [[otp,Client_ip]]}])
                                else:
                                        
                                        wks1.append_row([wks.cell(pos.row,1).value,form.email_id.data,otp,Client_ip])
                                return flask.render_template('index.html',form=form,message="Logged in Successfully",id=cipher_suite.encrypt(bytes(row[0],'UTF-8')),alert_colour=0)
                else:
                        if form.logincheckbox.data==True:
                                return flask.render_template('index.html',form=form,message="Please Register First!",alert_colour=1)
        else:
                return flask.render_template('index.html',form=form,alert_colour=-1)
@app.route('/account_creation',methods=['GET','POST'])
def account():
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1CyWjl6Y5Gi_e3z7A8wtw-qOaBe3GvCD4sqWWvaMubXY/edit?usp=sharing')
        wks=sh.worksheet("Client_Details")
        wks1=sh.worksheet("Client_Sessions")
        form = SignupForm(flask.request.form)
        if form.email_id.data:
                if form.email_id.data in wks.col_values(2):
                        return flask.render_template('index.html',form=form,alert_colour=1,message="You already have an account!")
                else:
                        time.sleep(random.randint(1,3))
                        OTP=random.randint(10000,99999)
                        id="CL"+datetime.now().strftime("%d%m%Y%H%M%S")
                        send_email(string.capwords(form.name.data)+' here is the otp for your Aptee account','registration_email.html',form.email_id.data.lower(),
                                param=[string.capwords(form.name.data),OTP,('127.0.0.1/account_creation/'+str(id))])
                        wks.append_row([id,form.email_id.data.lower(),string.capwords(form.name.data),
                                form.password.data,OTP,str(form.DOB.data),form.target.data,form.gender.data,form.college.data,form.college_location.data,form.course.data,form.semester.data])   
                        return flask.render_template('index.html',form=form,alert_colour=0,message="Account Created Successfully!",id=id)
        else:
               return flask.render_template('register.html',form=form) 
@app.route('/administrator_login',methods=['GET','POST'])
def admin_login():
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1CyWjl6Y5Gi_e3z7A8wtw-qOaBe3GvCD4sqWWvaMubXY/edit?usp=sharing')
        wks=sh.worksheet("Client_Details")
        wks1=sh.worksheet("Client_Sessions")
        Client_ip=flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.environ['REMOTE_ADDR'])
        form = SignupForm(flask.request.form)
        if form.email_id.data:
                if form.email_id.data in wks.col_values(2):
                        pos =wks.find(form.email_id.data.lower())
                        row =wks.row_values(pos.row)
                        if form.password.data!=row[3]:
                                return flask.render_template('admin_login.html',form=form,message="Password incorrect")
                        else:
                                otp=random.randint(10000,99999)
                                pos2=wks1.find(row[0])
                                if pos2:
                                        wks1.batch_update([{"range": "C"+str(pos2.row)+":D"+str(pos2.row), 
                                                                "values" : [[otp,Client_ip]]}])
                                else:
                                        
                                        wks1.append_row([wks.cell(pos.row,1).value,form.email_id.data,otp,Client_ip])
                                return flask.redirect(flask.url_for("admin_panel",id=cipher_suite.encrypt(bytes(str(otp)+','+wks.cell(pos.row,1).value,'UTF-8'))))
                                #return flask.render_template('admin.html',form=form,message="Logged in Successfully",id=wks.cell(pos.row,1).value)
                else:
                        return flask.render_template('admin_login.html',form=form,message="We couldnt find your email in our DB please contact Super Administrator")         
        else:
                return flask.render_template('admin_login.html',form=form)
@app.route('/admin_panel/<id>',methods=['GET','POST'])
def admin_panel(id):
        admin_id=str(cipher_suite.decrypt(bytes(id,'UTF-8')),'UTF-8').split(',')[1]
        otp=str(cipher_suite.decrypt(bytes(id,'UTF-8')),'UTF-8').split(',')[0]
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1CyWjl6Y5Gi_e3z7A8wtw-qOaBe3GvCD4sqWWvaMubXY/edit?usp=sharing')
        wks1=sh.worksheet("Client_Sessions")
        Client_ip=flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.environ['REMOTE_ADDR'])
        if admin_id in wks1.col_values(1):
                pos=wks1.find(admin_id)
                row =wks1.row_values(pos.row)
                if row[2]== otp and row[3]==Client_ip:
                        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1vYStVgetyDmsbZ-AXfiSvTRXwpTxsLaH4FFa1weFZ-I/edit?usp=sharing')
                        wks=sh.worksheet("Question_Details")
                        wks1=sh.worksheet("Tags_dir")
                        Question_subtopic = [[e[4], e[5]] for e in wks1.get_all_values()]
                        if flask.request.form:
                                Q_id='QA00000'
                                QNo=str(len(wks.col_values(1))+1)
                                Q_id=Q_id[:-len(QNo)]+str(QNo)
                                Question_Domain=','.join([i[:3] for i in flask.request.form.getlist('Q_Topic')])
                                Question_sub_Domain=','.join([i[:6] for i in flask.request.form.getlist('Q_Topic')])
                                Question_topics=','.join(flask.request.form.getlist('Q_Topic'))
                                wks.append_row([Q_id,flask.request.form.get('Q_img'),Question_Domain,Question_sub_Domain,Question_topics,
                                                flask.request.form.get('Q_lev'),flask.request.form.get('Q_Len'),flask.request.form.get('Q_title'),
                                                flask.request.form.get('Q_op_A'),flask.request.form.get('Q_op_B'),flask.request.form.get('Q_op_C'),flask.request.form.get('Q_op_D'),
                                                flask.request.form.get('Q_Sol'),flask.request.form.get('Sol_img'),flask.request.form.get('Sol_title'),(int(flask.request.form.get('Q_Len'))+int(flask.request.form.get('Q_lev')))*60])
                                return flask.render_template('admin.html',message="Submitted",id=id,tags=Question_subtopic)
                        else:   
                                return flask.render_template('admin.html',message="Logged in Successfully",id=id,tags=Question_subtopic)
                else:
                        return flask.redirect(flask.url_for("admin_login"))        
        else:
                return flask.redirect(flask.url_for("admin_login"))
@app.route('/contact_us',methods=['POST'])
def contact_us():
        form = SignupForm(flask.request.form)
        Client_ip=flask.request.environ.get('HTTP_X_FORWARDED_FOR', flask.request.environ['REMOTE_ADDR'])
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1CyWjl6Y5Gi_e3z7A8wtw-qOaBe3GvCD4sqWWvaMubXY/edit?usp=sharing')
        wks=sh.worksheet("Contact_us")
        print(flask.request.form)
        if flask.request.form:
                 wks.append_row([flask.request.form.get('name'),flask.request.form.get('email'),flask.request.form.get('subject'),
                 flask.request.form.get('body'),Client_ip,str(datetime.now())])      
        return flask.render_template('index.html',form=form,message="We have Received Your Message!",alert_colour=0)
@app.route('/comming_soon',methods=['GET'])
def comming_soon():
        form = SignupForm(flask.request.form)
        return flask.render_template('Comming_soon.html',form=form)
if __name__ == '__main__':
    app.run(debug = False,host='0.0.0.0')