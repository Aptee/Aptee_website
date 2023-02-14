import flask
import gspread
import keygenerator
from Form_model import SignupForm
import postgres
import random
profile= flask.Blueprint('profile', __name__,template_folder='Templates',static_folder='../Static')
gc = gspread.service_account_from_dict(keygenerator.get_db_auth())
@profile.route('/notif/<msg>&<alert>',methods=['GET','POST'])
@profile.route('/',methods=['GET','POST'])
def usr_profile(msg="",alert=0):
    form = SignupForm(flask.request.form)
    if 'id' in flask.session:
        postgres_find_query="""with coins as (SELECT c.clientid, sum(c.coin_in::INTEGER)-sum(c.coin_out::INTEGER) as coin from clients.coin_history c
                                WHERE c.clientid like '{0}'               
                                GROUP by c.clientid)
                                SELECT d.clientid,d.email_id,d.client_name,d.cl_password,d.dob::TIMESTAMP::DATE,d.target_exam,d.gender,d.college,d.college_location,d.client_course,d.semester,d.avatar,d.email_verified,co.coin from clients.details as d
                                LEFT JOIN coins co on d.clientid = co.clientid
                                WHERE d.clientid like '{0}'
                                LIMIT 1;""".format(flask.session['id'])
        res,err=postgres.postgres_connect(postgres_find_query,commit=0)
        if len(err)==0:
            client=[list(e) for e in res]
            client=client[0]
        #print(client)
        if len(client[-2]):
            verify=1
        else:
            verify=0
        postgres_find_query="""
        SELECT att.questionid,att.question_subtopic,att.question_level,att.time_taken,att.correct from clients.attempts att
        where att.clientid like '{0}' and att.correct::BOOLEAN = FALSE
        ORDER by att.attempt_time DESC,att.question_level ASC
        LIMIT 4
        """.format(flask.session['id'])
        res,err=postgres.postgres_connect(postgres_find_query,commit=0)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1hSXNatvksQJBg-O0deeBMZyGQt08_iX41bX0LsQ2IBc/edit?usp=sharing')
        wks=sh.worksheet("Blogs")
        row =wks.row_values(2)

        if len(err)==0:
            questions=[list(e) for e in res]
            print(questions)
        if len(msg)==0:
            return flask.render_template('Profile.html',Data=client,form=form,id=flask.session['id'],verify=verify,Ques=questions,row=row)
        else:
            return flask.render_template('Profile.html',Data=client,form=form,id=flask.session['id'],verify=verify,Ques=questions,row=row,message=msg,alert_colour=alert)
    else:
        return flask.redirect(flask.url_for("home"))
@profile.route('/Report',methods=['GET','POST'])
def usr_report_menu():
    if 'id' in flask.session:
        form = SignupForm(flask.request.form)
        query="""
        SELECT a.test_id,a.attempt_time::TIMESTAMP::DATE,a.clientid from clients.attempts a
        WHERE a.clientid LIKE '{0}' and a.test_id LIKE '%TI%'
        GROUP by a.test_id,a.attempt_time::TIMESTAMP::DATE,a.clientid
        """.format(flask.session['id'])
        res,err=postgres.postgres_connect(query,commit=0)
        if len(err)==0:
            data=[[e[0],e[1].strftime("%d-%m-%Y"),e[2]] for e in res]
        print(data)
        return flask.render_template('Report.html',Data=data,form=form,id=flask.session['id'])
        #query attempts to find distinct test and group by date
    else:
        return flask.redirect(flask.url_for("home"))
@profile.route('/Test_Report/id=<uid>&date=<date>',methods=['GET','POST'])
def usr_report_tid(uid,date):
    form = SignupForm(flask.request.form)
    if 'id' in flask.session:
        if uid[:2] == 'TI':
            query="""SELECT a.clientid,a.questionid,a.correct,a.submitted,concat('Level ',a.question_level) as question_level,a.question_length,a.question_subtopic,a.attempt_time::TIMESTAMP::DATE,a.time_taken from clients.attempts a
                    WHERE a.clientid like '{0}' 
                    and a.attempt_time::TIMESTAMP::DATE =to_date('{1}','DD-MM-YYYY') 
                    and a.test_id ='{2}'""".format(flask.session['id'],date,uid)
            res,err=postgres.postgres_connect(query,commit=0)
            if len(err)==0:
                Attempts=[list(e) for e in res]
                return flask.render_template('Test_Report.html',form=form,id=flask.session['id'],
                                                bar_chart=','.join(Bar_chart(Attempts)),
                                                pie=','.join(pie_chart(Attempts,2)),pie2=','.join(pie_chart(Attempts,4)))
        #use forms to get test id and date
        #query attempts to find test and date
        
    else:
        return flask.redirect(flask.url_for("home"))
@profile.route('/analysis',methods=['GET','POST'])
def usr_analysis():
    form = SignupForm(flask.request.form)
    if 'id' in flask.session:
        query="""with coins as (SELECT c.clientid, sum(c.coin_in::INTEGER)-sum(c.coin_out::INTEGER) as coin from clients.coin_history c
                GROUP by c.clientid)
                SELECT a.clientid,a.questionid,a.correct,a.submitted,concat('Level ',a.question_level) as question_level,a.question_length,a.question_subtopic,a.attempt_time::TIMESTAMP::DATE,a.time_taken,d.client_name,co.coin from clients.attempts a LEFT JOIN clients.details d 
                on a.clientid=d.clientid
                LEFT JOIN coins co on co.clientid=a.clientid
                WHERE a.clientid like '{0}' and a.attempt_time::TIMESTAMP::DATE > to_date('{1}','DD-MM-YYYY')""".format(flask.session['id'],'01-01-2023')
        res,err=postgres.postgres_connect(query,commit=0)
        if len(err)==0:
            client=[list(e) for e in res]
            Attempts=[x[:-2] for x in client]
            client=client[0][-2:]
            unique_q=[X[1] for X in Attempts]
        #query attempts to find all questions
        #print(Attempts)
        return flask.render_template('Analysis.html',form=form,id=flask.session['id'],
        bar_chart=','.join(Bar_chart(Attempts)),
        Time1=','.join(calendar_chart(Attempts)),pie=','.join(pie_chart(Attempts,2)),pie2=','.join(pie_chart(Attempts,4)),Total=len(Attempts))
    else:
        return flask.redirect(flask.url_for("home"))
@profile.route('/Coin_history/',methods=['GET','POST'])
@profile.route('/Coin_history/Page=<page>',methods=['GET','POST'])
def usr_coin_history(page=0):
    form = SignupForm(flask.request.form)
    try:
        page=int(page)
    except:
        page=0
    if 'id' in flask.session:
        query="""
        SELECT * from clients.coin_history co
        WHERE co.clientid = '{0}'
        ORDER BY co.transaction_time DESC 
        OFFSET {1}
        Limit 10;
        """.format(flask.session['id'],int(page)+10)
        res,err=postgres.postgres_connect(query,commit=0)
        if len(err)==0:
            data=[[a[1],a[2],a[3],a[4],a[5].strftime("%m/%d/%Y %H:%M:%S")] for a in res]
        
        return flask.render_template('coin_history.html',Data=data,form=form,id=flask.session['id'])
    else:
        return flask.redirect(flask.url_for("home"))
def calendar_chart(Attempts):
    TimeS=[a[7].strftime("%m/%d/%Y") for a in Attempts]
    countS = {item:TimeS.count(item) for item in TimeS}
    TimeS=sorted(countS.items(), key=lambda x:x[1],reverse=True)
    countS=[[a[0],a[1]] for a in TimeS]
    countS=[str(j) for sub in countS for j in sub]
    return countS
def pie_chart(Attempts,index=2):
    #print(Attempts)
    if index==2:
        TimeS=[a[index] if a[3]=='1' else 'Skipped' for a in Attempts] 
    else:   
        TimeS=[a[index] for a in Attempts]
    pie= {item:TimeS.count(item) for item in TimeS}
    TimeS=sorted(pie.items(), key=lambda x:x[1],reverse=True)
    pie=[[a[0],a[1]] for a in TimeS]
    pie.insert(0,['Labels','Counts'])
    pie=[str(j) for sub in pie for j in sub]
    print(pie)
    return pie
def Bar_chart(Attempts):
    dir=[['BL1','Numbers'], ['BL2','Averages and Mixtures'], ['BL3','Arithmatic and Word Based Problems'], ['BL4','Geometry'], 
    ['BL5','Algebra'], ['BL6','Counting']]
    data=[['Topic','Correct','In Correct']]
    BlockT=[a[6].split(',') for a in Attempts if a[2]=='True']
    BlockT=[j[:3] for sub in BlockT for j in sub]
    BlockF=[a[6].split(',') for a in Attempts if a[2]=='False']
    BlockF=[j[:3] for sub in BlockF for j in sub]
    countsT = {item:BlockT.count(item) for item in BlockT}
    BlockT=sorted(countsT.items(), key=lambda x:x[1],reverse=True)
    #print(BlockT)
    countsF = {item:BlockF.count(item) for item in BlockF}
    BlockF=sorted(countsF.items(), key=lambda x:x[1],reverse=True)
    #print(BlockF)
    correct=[['BL1',0],['BL2',0],['BL3',0],['BL4',0],['BL5',0],['BL6',0]]    
    incorrect=[['BL1',0],['BL2',0],['BL3',0],['BL4',0],['BL5',0],['BL6',0]]
    for a in BlockF:
        incorrect[incorrect.index([a[0],0])][1]=a[1]
    for a in BlockT:
        correct[correct.index([a[0],0])][1]=a[1]    
    for i in range(1,7):
        data.append([dir[i-1][1],correct[i-1][1],incorrect[i-1][1]])
    data=[str(j) for sub in data for j in sub]    
    #print(data)
    return data