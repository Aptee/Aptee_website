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
    if 'id' in flask.session:
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1hSXNatvksQJBg-O0deeBMZyGQt08_iX41bX0LsQ2IBc/edit?usp=sharing')
        wks=sh.worksheet("Blogs")

        #randomlist = random.sample(range(10, 30), 5)
        #row =wks.row_values(2)
        row=wks.batch_get(['A3:L4'])
        if len(msg)==0:
            return flask.render_template('Blog_homepage.html',form=form,Blog_list=row[0],id=flask.session['id'])
        else:
            return flask.render_template('Blog_homepage.html',form=form,Blog_list=row[0],message=msg,alert_colour=alert)
    else:
        return flask.render_template('Blog_homepage.html',form=form,Blog_list=row[0])
@blog.route('/Post/<postid>')
def blog_post(postid=""):
    form = SignupForm(flask.request.form)
    if 'id' in flask.session:
        if len(postid)==0:
            return flask.redirect(flask.url_for("blog.blog_home",msg="Sorry We cannot Display that Blog",alert=0))
        else:
            sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1hSXNatvksQJBg-O0deeBMZyGQt08_iX41bX0LsQ2IBc/edit?usp=sharing')
            wks=sh.worksheet("Blogs")
            #print(postid)
            if postid[:2]=='BG':
                blog_row=int(postid[2:])+1
            row =wks.row_values(blog_row)
            Topic_names=keygenerator.get_questions_topics(row[4].split(','))
            print(row[4])
            print([x[1] for x in Topic_names])
            if flask.request.form:
                pass
            #print(row)
            return flask.render_template('blog_post.html',form=form,Question=','.join([x[1] for x in Topic_names]),Blog=row,id=flask.session['id'])
    else:
        return flask.render_template('blog_post.html',form=form,Blog=row)
