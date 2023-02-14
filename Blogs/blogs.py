import flask
import gspread
import keygenerator
from Form_model import SignupForm
import postgres
import random
blog= flask.Blueprint('blog', __name__,template_folder='Template',static_folder='../Static')
gc = gspread.service_account_from_dict(keygenerator.get_db_auth())

@blog.route('/notif/<msg>&<alert>',methods=['GET','POST'])
@blog.route('/',methods=['GET','POST'])
def blog_home(msg="",alert=0):
    form = SignupForm(flask.request.form)
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1hSXNatvksQJBg-O0deeBMZyGQt08_iX41bX0LsQ2IBc/edit?usp=sharing')
    wks=sh.worksheet("Blogs")
    #randomlist = random.sample(range(10, 30), 5)
    row =wks.row_values(2)


    if len(msg)==0:
        return flask.render_template('blogquestion.html',form=form,Blog_list=row)
    else:
        return flask.render_template('blogquestion.html',form=form,Blog_list=row,message=msg,alert_colour=alert)
@blog.route('/Post/<postid>')
def blog_post(postid=""):
    if len(postid)==0:
        return flask.redirect(flask.url_for("blog.blog_home",msg="Sorry We cannot Display that Blog",alert=0))
    else:
        form = SignupForm(flask.request.form)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1hSXNatvksQJBg-O0deeBMZyGQt08_iX41bX0LsQ2IBc/edit?usp=sharing')
        wks=sh.worksheet("Blogs")
        #print(postid)
        if postid[:2]=='BG':
            blog_row=int(postid[2:])+1
        row =wks.row_values(blog_row)
        #print(row)
        return flask.render_template('bloganswer.html',form=form,Blog=row)
