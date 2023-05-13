import flask
import gspread
import keygenerator
from Form_model import SignupForm
import postgres
import random
import time
import json
import requests

ecm= flask.Blueprint('ecm', __name__,template_folder='../Templates',static_folder='../Static')
gc = gspread.service_account_from_dict(keygenerator.get_db_auth())

@ecm.route('/cart/',methods=['POST'])
def cart():
    if 'id' in flask.session:
        print(1)
        if flask.request.form:
            postgres_find_query="""with coins as (SELECT c.clientid, sum(c.coin_in::INTEGER)-sum(c.coin_out::INTEGER) as coin from clients.coin_history c
                                    WHERE c.clientid like '{0}'               
                                    GROUP by c.clientid)
                                    SELECT d.clientid,d.email_id,d.client_name,d.cl_password,d.dob::TIMESTAMP::DATE,d.target_exam,d.gender,d.college,d.college_location,d.client_course,d.semester,d.avatar,d.email_verified,co.coin from clients.details as d
                                    LEFT JOIN coins co on d.clientid = co.clientid
                                    WHERE d.clientid like '{0}'
                                    LIMIT 1;""".format(flask.session['id'])
            res,err=postgres.postgres_connect(postgres_find_query,commit=0)
            print(2)
            if len(err)==0:
                client=[list(e) for e in res]
                client=client[0]
                print(3)
            if len(client[-2])==0:
                print(4)
                product_name=flask.request.form.get('product')
                pay_with_coin=flask.request.form.get('ap_coin')
                if pay_with_coin:
                    url = 'http://127.0.0.1:8000/api/purchase_through_coins'
                    payload={
                                "id":flask.session['id'],
                                "email":client[1],
                                "product_id":flask.request.form.get('product_id'),
                                "price":flask.request.form.get('price'),
                                "como_id":flask.request.form.get('como_id')

                        }
                    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                    # json.dumps(payload)
                    r = requests.post(url, data=json.dumps(payload), headers=headers)
                    if r.status_code == 200:
                        return flask.render_template('cart.html',id=flask.session['id'],message="Purchase Successful",product_name=product_name,link=r.json()) 
                    elif r.status_code == 400:
                        return flask.render_template('cart.html',id=flask.session['id'],message="Purchase Failed",product_name=product_name,link=r.json())
            else:
                return flask.render_template('cart.html',id=flask.session['id'],message="Please Verify Email First")
        else:
            return "no form"
    else:
        return "no id login"
@ecm.route('/reattempt_questions/',methods=['POST'])
def reat_questions(otp=0):
    if flask.request.form and 'id' in flask.session:
        postgres_find_query="""
                SELECT od.id,od.od_token,od.comodity_id,od.complition_otp,cd.email_id,cd.client_name from ecommerce.orders od 
                left join clients.details cd
                on cd.clientid= od.client_id
                WHERE od.od_token='{0}'
                """.format(flask.request.form['od_token'])
        res,err=postgres.postgres_connect(postgres_find_query,commit=0)
        print(flask.request.form['od_token'],res)
        details=[list(e) for e in res]
        if len(details)>0:
            details=details[0]
        url = 'http://127.0.0.1:8000/send_email'
        payload={
                    "id":flask.session['id'],
                    "header":details[5]+ " Here is the Question You Asked For",
                    "emails":details[4],
                    "email_template":'Reattempt_Question.html',
                    "param":details[5]+'||'+flask.url_for("test.daily",qid=details[2],Mobile=0,Token=str(flask.request.form['od_token']))
            }
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        # json.dumps(payload)
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if r.status_code==200:
            return flask.redirect(flask.url_for("profile.usr_profile",msg="Email Sent",alert=0))
        else:
            return flask.redirect(flask.url_for("profile.usr_profile",msg="Error in Sending Email Link",alert=0))
    else: 
        return flask.redirect(flask.url_for("profile.usr_profile",msg="Error in Sending Email Link",alert=0))
