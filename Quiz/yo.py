#question_no=len(flask.request.form.get('Q_status').split(','))-1
            #if question_no>=len(q_id):
            #    return flask.render_template('select_exam.html',form=form,message="You Have completed the test",alert_colour=1)
            #test_row=int(q_id[question_no][2:])+1
            #row =wks.row_values(test_row)
            #if flask.request.form.get('Q_time'):
            
            #    if flask.request.form.get('mcq')==row[12]:
            #        correct=True
            #    else:
            #        correct=False
            #    postgres_insert_query = """
            #                                INSERT INTO clients.attempts(questionid,clientid,attempt_time,correct,time_taken,optimum_time,question_subtopic,question_level,question_length,submitted)
            #                                VALUES ('{0}','{1}',CURRENT_TIMESTAMP,'{2}','{3}','{4}','{5}','{6}','{7}',{8})
            #                                """.format(row[0],flask.session['id'],correct,(int(flask.request.form.get('Q_time'))/1000),\
            #                                                                 row[15],row[4],row[5],row[6],flask.request.form.get('Q_status').split(',')[-1])
             #   print(postgres_insert_query)
            #return flask.render_template('exam_dashboard.html',Quiz=1,Ques=row,Timer=row[15],Questions=flask.request.form.get('Q_id'),\
            #        submit=flask.request.form.get('Q_status'),Question_no=question_no+1,Ques_id=row[0],check=flask.request.form.get('Q_check'),form=form)
                  function clearForm(){
        document.getElementById("op1").checked = false;
        document.getElementById("op2").checked = false;
        document.getElementById("op3").checked = false;
        document.getElementById("op4").checked = false;
      }

@test.route('/exam_dashboard/',methods=['GET','POST'])
def exam_dashboard():
    form = SignupForm(flask.request.form)
    if 'id' not in flask.session:
        flask.session['page']='test'
        return flask.render_template('select_exam.html',form=form,message="Please Login to Continue!",alert_colour=0)
    else:
        if flask.request.form:
            skip=1
            sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1vYStVgetyDmsbZ-AXfiSvTRXwpTxsLaH4FFa1weFZ-I/edit?usp=sharing')
            wks=sh.worksheet("Question_Details")
            q_id=flask.request.form.get('Q_ids').split(',')
            status=flask.request.form.get('Q_status').split(',')
            print(q_id)
            print(status)
            row=flask.request.form.get('row')
            print(row)
            if len(q_id)==1:
                return flask.render_template('select_exam.html',form=form,message="You Have completed the test",alert_colour=1)
            if flask.request.form.get('Q_Time')!= None:
                time=flask.request.form.get('Q_Time')
                if flask.request.form.get('mcq') == None:
                    skip=0
                elif flask.request.form.get('mcq')==row[12]:
                    correct=True
                else:
                    correct=False
                status[-1]=skip
                postgres_insert_query = """
                                            INSERT INTO clients.attempts(questionid,clientid,attempt_time,correct,time_taken,optimum_time,question_subtopic,question_level,question_length,submitted)
                                            VALUES ('{0}','{1}',CURRENT_TIMESTAMP,'{2}','{3}','{4}','{5}','{6}','{7}',{8})
                                            """.format(row[0],flask.session['id'],correct,(int(flask.request.form.get('Q_time'))/1000),\
                                                                             row[15],row[4],row[5],row[6],flask.request.form.get('Q_status').split(',')[-1])

            row=wks.row_values(3)
            
            return flask.render_template('exam_dashboard.html',Quiz=1,Ques=row,Timer=row[15],Questions=flask.request.form.get('Q_id'),\
                    submit=0,Question_no=1,Q_id=q_id[-2],check=','.join(status),status=status.split(',')[1:],form=form)

        var endTime = Date.now();
        var difference = endTime - startTime - 1000;
        var Questions='{{Questions}}';
        var arr=Questions.split(',');
        arr.pop();
        var status='{{status}}'
        document.getElementById("feild_time").value = String(qid)+','+String(difference);
        document.getElementById("feild_stack").value = arr;
        document.getElementById("feild_det").value = String(status)+',0';