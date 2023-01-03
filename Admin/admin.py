import flask
import gspread
import keygenerator
import datetime
import postgres
from Form_model import SignupForm
admin= flask.Blueprint('admin', __name__,template_folder='Templates')

gc = gspread.service_account_from_dict(keygenerator.get_db_auth())

@admin.route('/administrator_login',methods=['GET','POST'])
def admin_login():
        form = SignupForm(flask.request.form)
        if 'id' in flask.session:
                id=flask.session['id']
                if id[:3]!='ADM':
                        return flask.redirect(flask.url_for("home"))
                else:
                        return flask.redirect(flask.url_for("admin.question_crud"))
        else:
                if form.email_id.data:
                        postgres_find_query="""
                                with df as (SELECT * from clients.details det 
                                WHERE det.email_id like '{0}'
                                ),
                                df2 as (
                                SELECT * from clients.details d 
                                order by REPLACE(d.clientid,'ADM','')::INTEGER desc
                                LIMIT 1
                                )
                                SELECT * from df
                                UNION ALL
                                SELECT * from df2
                        """.format(form.email_id.data)
                        res,err=postgres.postgres_connect(postgres_find_query,commit=0)
                        details=[list(e) for e in res]
                       
                        if len(details)==2:
                                if len(err)==0 and form.password.data!=details[0][3]:
                                        return flask.render_template('admin_login.html',form=form,message="Password incorrect")
                                elif len(err)==0 and form.password.data==details[0][3]:
                                        
                                        if details[0][0][:3]=='ADM':
                                                flask.session['id']=details[0][0]
                                                flask.session['last_id']=details[1][0]
                                                AdId=str(int((flask.session['last_id'])[3:])+1)
                                                flask.session['last_id']=(flask.session['last_id'])[:-len(AdId)]+AdId
                                                return flask.redirect(flask.url_for("admin.question_crud"))
                                        else:
                                                return flask.render_template('admin_login.html',form=form,message="You are not an admin please contact Super Administrator")
                        else:
                                return flask.render_template('admin_login.html',form=form,message="We couldnt find your email in our DB please contact Super Administrator")         
        
        return flask.render_template('admin_login.html',form=form,message="")
        
@admin.route('/admin_panel/',methods=['GET','POST'])
def question_crud():
        if 'id' in flask.session:
                sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1vYStVgetyDmsbZ-AXfiSvTRXwpTxsLaH4FFa1weFZ-I/edit?usp=sharing')
                wks=sh.worksheet("Question_Details")
                wks2=sh.worksheet("Tags_dir")
                Question_subtopic = [[e[4], e[5]] for e in wks2.get_all_values()]
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
                        return flask.render_template('add_questions.html',message="Submitted",tags=Question_subtopic[1:])
                else:   
                        return flask.render_template('add_questions.html',message="Logged in Successfully",tags=Question_subtopic[1:])
        else:
                return flask.redirect(flask.url_for("admin.admin_login"))        
@admin.route('/administrators/modid=<mod>', methods=['GET','POST'])
def administrator(mod='0'):
        if 'id' in flask.session:
                if mod=='0':
                        #print(mod)
                        #print(flask.session['last_id'])
                        if flask.request.form:
                                postgres_insert_query="""INSERT INTO clients.details (clientid,email_id,client_name,cl_password,dob,target_exam,gender,college,college_location,client_course,semester,avatar,coins)
                                        VALUES ('{0}','{1}','{2}','{3}',CURRENT_DATE,'GATE','MALE','DETS','Kalyani','Btech','7','NONE','0')
                                        """.format(flask.request.form.get('Admin_id'),flask.request.form.get('Admin_email'),flask.request.form.get('Admin_name'),\
                                                flask.request.form.get('Admin_pass'))
                                a=postgres.postgres_connect(postgres_insert_query,commit=1)
                                if a:
                                        AdId=str(int((flask.session['last_id'])[3:])+1)
                                        flask.session['last_id']=(flask.session['last_id'])[:-len(AdId)]+AdId
                                        return flask.render_template('client_crud.html',message="Submitted",Next_ID=flask.session['last_id'])
                                else:
                                        return flask.render_template('client_crud.html',message="Failed",Next_ID=flask.session['last_id']) 
                        else:
                                return flask.render_template('client_crud.html',message="fill new admin details",Next_ID=flask.session['last_id'])
                else:
                        return flask.render_template('client_crud.html',message="yo",Next_ID=flask.session['last_id'])
        else:
                return flask.redirect(flask.url_for("admin_login"))   

@admin.route('/logout',methods=['GET','POST'])
def logout():
        flask.session.pop('id',None)
        flask.session.pop('last_id',None)
        return flask.redirect(flask.url_for("admin.admin_login"))
