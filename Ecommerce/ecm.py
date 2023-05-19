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
        form = SignupForm(flask.request.form)
        if flask.request.form:
            postgres_find_query="""with coins as (SELECT c.clientid, sum(c.coin_in::INTEGER)-sum(c.coin_out::INTEGER) as coin from clients.coin_history c
                                    WHERE c.clientid like '{0}'               
                                    GROUP by c.clientid)
                                    SELECT d.clientid,d.email_id,d.client_name,d.cl_password,d.dob::TIMESTAMP::DATE,d.target_exam,d.gender,d.college,d.college_location,d.client_course,d.semester,d.avatar,d.email_verified,co.coin from clients.details as d
                                    LEFT JOIN coins co on d.clientid = co.clientid
                                    WHERE d.clientid like '{0}'
                                    LIMIT 1;""".format(flask.session['id'])
            res,err=postgres.postgres_connect(postgres_find_query,commit=0)
            # print(2)
            if len(err)==0:
                client=[list(e) for e in res]
                client=client[0]
                # print(3)
            if len(client[-2])==0:
                # print(4)
                product_name=flask.request.form.get('product')
                pay_with_coin=flask.request.form.get('ap_coin')
                if pay_with_coin:
                    url = 'https://aptee.onrender.com/api/purchase_through_coins'
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
                        return flask.render_template('Order_successful.html',form=form,id=flask.session['id'],product_id=flask.request.form.get('product_id'),Price=flask.request.form.get('price'),product_name=product_name,link=r.json()) 
                    elif r.status_code == 400:
                        return flask.render_template('Order_successful.html',form=form,id=flask.session['id'],message="Purchase Failed",product_name=product_name,link=r.json())
            else:
                return flask.render_template('Order_successful.html',form=form,id=flask.session['id'],message="Please Verify Email First")
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
        #print(flask.request.form['od_token'],res)
        details=[list(e) for e in res]
        if len(details)>0:
            details=details[0]
        url = 'https://aptee.onrender.com/send_email'
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
@ecm.route('/reattempt_quiz/',methods=['POST'])
def reat_quiz(otp=0):
    if flask.request.form and 'id' in flask.session:
        postgres_find_query="""
                SELECT od.id,od.od_token,od.comodity_id,od.complition_otp,cd.email_id,cd.client_name,od.product_id from ecommerce.orders od 
                left join clients.details cd
                on cd.clientid= od.client_id
                WHERE od.od_token='{0}'
                """.format(flask.request.form['od_token'])
        res,err=postgres.postgres_connect(postgres_find_query,commit=0)
        #print(flask.request.form['od_token'],res)
        details=[list(e) for e in res]
        if len(details)>0:
            details=details[0]
        if details[6] == '10':
            url = 'https://aptee.onrender.com/Generate_tests'
            payload={
                    "id":flask.session['id'],
                    "header":details[5]+ " Here is the Quiz You Asked For",
                    "emails":details[4],
                    "email_template":'Reattempt_Question.html',
                    "param":details[5]+'||'+flask.url_for("test.customTest",testId=details[2])
            }
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            # json.dumps(payload)
            r = requests.post(url, data=json.dumps(payload), headers=headers)    
        url = 'https://aptee.onrender.com/send_email'
        payload={
                    "id":flask.session['id'],
                    "header":details[5]+ " Here is the Quiz You Asked For",
                    "emails":details[4],
                    "email_template":'Reattempt_Question.html',
                    "param":details[5]+'||'+flask.url_for("test.customTest",testId=details[2])
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

@ecm.route('/purchase_coins/<cid>&<coupon>',methods=['GET','POST'])
def purchase(cid='0',coupon=""):
    form = SignupForm(flask.request.form)
    if 'id' in flask.session and len(coupon)!=0:
        print(10)
        postgres_find_query="""SELECT a1.coupon_code,a1.product_id,a1.price_disc,a1.expired,cd.clientid,cd.client_name,cd.email_id from (SELECT *,split_part(cp.coupon_code,'-',4) as cl_id from ecommerce.coupons cp) a1
left join clients.details cd on cd.clientid = a1.cl_id WHERE coupon_code='{0}';""".format(coupon)
        res,err=postgres.postgres_connect(postgres_find_query,commit=0)
        details=[list(e) for e in res]
        if len(details)==0:
            return flask.render_template('.html',form=form,id=flask.session['id'],message="Invalid Coupon")
        else:
            details=details[0]
        if details[3]=='0':
            print(details)
            url = 'https://aptee.onrender.com/api/purchase_through_coupons'
            payload={
                        "id":cid,
                        "email":details[6],
                        "product_id":details[1],
                        "coupon":coupon,
                        "price":details[2],
                        "como_id":'cb'+str(details[1]),
                        "name":details[5]
            }
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            # json.dumps(payload)
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            if r.status_code==200:
                url = 'https://aptee.onrender.com/send_email'
                payload={
                            "id":cid,
                            "header":details[5]+ " HERE ARE YOUR COINS!",
                            "emails":details[6],
                            "email_template":'Purchase_confirmation.html',
                            "param":details[5]+'||'+"YOUR PRODUCT"
                    }
                headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                # json.dumps(payload)
                r = requests.post(url, data=json.dumps(payload), headers=headers)
                # return flask.render_template('Product_buy_page.html',form=form,id=flask.session['id'],message="Please Verify Email First")
                return flask.render_template('Order_successful.html',form=form,id=flask.session['id'],product_id=details[1],Price='Rs. '+str(details[2]),product_name=str(20*int(details[2]))+' Aptee Coins',coins='1',success='1') 

            else:
                return flask.redirect(flask.url_for("profile.usr_profile",msg="Error In Completing Purchase",alert=0))
        else:
            # return flask.render_template('Product_buy_page.html',form=form,id=flask.session['id'],message="Expired Coupon")
            return flask.redirect(flask.url_for("profile.usr_profile",msg="Your Coupon has expired",alert=0))
    else:
        return flask.redirect(flask.url_for("profile.usr_profile",msg="Error In Completing Purchase",alert=0))
@ecm.route('/order_status/return?link_id=<link_id>&success=<success>&<buf>',methods=['GET','POST'])
def confirm_purchase(link_id="",success=1,buf=""):
    form = SignupForm(flask.request.form)
    if 'id' in flask.session:
        return flask.render_template('Orders_Status.html',form=form,id=flask.session['id'],link_id=link_id,success=success)
    else:
        return flask.render_template('Orders_Status.html',form=form,link_id=link_id,success=success)

@ecm.route('/Buy_product/item_id=<item>',methods=['GET','POST'])
@ecm.route('/Buy_product/',methods=['GET','POST'])
def buy_product(item=0):
    form = SignupForm(flask.request.form)
    if 'id' in flask.session and flask.request.form:
        postgres_find_query="""with coins as (SELECT c.clientid, sum(c.coin_in::INTEGER)-sum(c.coin_out::INTEGER) as coin from clients.coin_history c
                                    WHERE c.clientid like '{0}'               
                                    GROUP by c.clientid)
                                    SELECT d.clientid,d.email_id,d.client_name,d.cl_password,d.dob::TIMESTAMP::DATE,d.target_exam,d.gender,d.college,d.college_location,d.client_course,d.semester,d.avatar,d.email_verified,co.coin from clients.details as d
                                    LEFT JOIN coins co on d.clientid = co.clientid
                                    WHERE d.clientid like '{0}'
                                    LIMIT 1;""".format(flask.session['id'])
        res,err=postgres.postgres_connect(postgres_find_query,commit=0)
        # print(2)
        if len(err)==0:
            client=[list(e) for e in res]
            client=client[0]
            # print(3)
        if len(client[-2])!=0:
            return flask.redirect(flask.url_for("profile.usr_profile",msg="Please Verify Your Email Address to Purchase",alert=0))
        url = 'http://127.0.0.1:8000/api/cashfree_payments'
        payload={
                    "id":client[0],
                    "email":client[1],
                    "product_id":'PD_'+flask.request.form.get('product_id'),
                    "coupon":flask.request.form.get('coupon_id'),
                    "price":flask.request.form.get('price'),
                    "name":client[2]
        }
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        # json.dumps(payload)
        print(payload)
        #r = requests.post(url, data=json.dumps(payload), headers=headers)
    else:
        if item!=0:
            print(item)
            data=keygenerator.get_shop_products(item=item)
            return flask.render_template('Product.html',form=form,data=data)
        else:
            return flask.redirect(flask.url_for("usr_shop"))