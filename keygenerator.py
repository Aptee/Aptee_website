from cryptography.fernet import Fernet
import urllib.request
def generatekey():
    f = open("etc/secrets/det.txt", "r")
    a=f.read()
    return a[2:]
def cashpay_auth():
    f = open("etc/secrets/cashfree.txt", "r")
    a=f.read()
    return a.split(',')
def get_db_auth():
    cipher_suite = Fernet(bytes(generatekey(),'UTF-8'))
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
    return auth
def get_email_pass():
    cipher_suite = Fernet(bytes(generatekey(),'UTF-8'))
    return str(cipher_suite.decrypt(bytes('gAAAAABivcvM07hd5UvYq-h_Qi3_AXivMrKkhaWqvzzvlQ0PFffl4pk7tF7JpYCvADHYZITI53DDANHAvdheAdCwLR1Lmd2pPYonRE4QrPrCAh_6xUanbGo=','UTF-8')),'UTF-8')
#print(generatekey())
def get_Test_names(Tid=[]):
    line=urllib.request.urlopen('https://raw.githubusercontent.com/Aptee/Aptee_Data/main/Test_data/Test_name.csv').read()
    rec=[e.split(',') for e in str(line,'utf-8').split('\n')]
    if len(Tid)>1:
        result = [element for element in rec if element[0] in Tid]
    elif len(Tid)==1:
        result = [element for element in rec if element[0] in str(Tid)]
    else:
        print('Error')
    return result
def get_questions_topics(id=[]):
    line=urllib.request.urlopen('https://raw.githubusercontent.com/Aptee/Aptee_Data/main/Test_data/Qtags_dir.csv').read()
    rec=[e.split(',') for e in str(line,'utf-8').split('\n')]
    if len(id)>1:
        result = [element for element in rec if element[0] in id]
    elif len(id)==1:
        result = [element for element in rec if element[0] in str(id)]
    else:
        print('Error')
    return result
def get_rec_questions(Tid=[],rec=0):
    if rec==0:
        line=urllib.request.urlopen('https://raw.githubusercontent.com/Aptee/Aptee_Data/main/Test_data/AntiRecommendations.csv').read()
    else:
        line=urllib.request.urlopen('https://raw.githubusercontent.com/Aptee/Aptee_Data/main/Test_data/Recommendations.csv').read()
    rec=[e.split(',') for e in str(line,'utf-8').split('\n')]
    rec=[element for element in rec if len(element)>1]
    if len(Tid)>9:
        result = [element[2:] for element in rec if element[1] in Tid]
        # print(result)
        flatten_lst=lambda y:[x for a in y for x in flatten_lst(a)] if type(y) is list else [y]
        result=flatten_lst(result)
        counts = {item:result.count(item) for item in result}
        items=sorted(counts.items(), key=lambda x:x[1],reverse=True)
        # print(items)
        result=[x[0] for x in items]
        try:
            result=result[:15]
        except:
            return {'msg':'We Couldnt Find 15 Different Questions you got wrong To Built a Test Out Off!'}
    else:
        return {"msg":"Minimum 10 Questions Required"}
    return result
def get_shop_products(item=0):
    line=urllib.request.urlopen('https://raw.githubusercontent.com/Aptee/Aptee_Data/main/Test_data/Products_with_img.csv').read()
    rec=[e.split(',') for e in str(line,'utf-8').split('\n')]
    if len(rec)>1 and item!=0:
        result = rec[1:-1]
        result=[x for x in rec if x[0]==str(item)][0]
        return result
    elif len(rec)>1 and item==0:
        result = rec[1:-1]
        return result
    else:
        return "error"
        #print(result) 