import pickle
import cv2 
import pyrebase
import numpy as np
from flask_login import login_required, logout_user
from flask import Flask, render_template, redirect, url_for, request, flash
from ImageProcessing import imageProcessing



##### APP CONFIGRATIONS #####

# initialize app
app = Flask(__name__)
USERNAME =""


# Firebase Configs
firebaseConfig = {
                'apiKey': "AIzaSyDohHMrf-w7xVRsPSV29V_pBPGXHh6mF4Q",
                'authDomain': "jd-ml-gp.firebaseapp.com",
                'databaseURL': "https://jd-ml-gp-default-rtdb.firebaseio.com",
                'projectId': "jd-ml-gp",
                'storageBucket': "jd-ml-gp.appspot.com",
                'messagingSenderId': "1085152223095",
                'appId': "1:1085152223095:web:789e7383a34e8008398b72",
                'measurementId': "G-GWELVK4C0H"
                }
## Firebase Connection
firebase = pyrebase.initialize_app(firebaseConfig)
db_data = firebase.database()
db_auth = firebase.auth()

# AI Connection
filename = 'MODEL/model.pkl'
classifier = pickle.load(open(filename, 'rb'))

##############################

# Routings
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/checkcase')
def check_case():
    cla = USERNAME
    return render_template('checkcase2.html',
                           user_name=cla)

@app.route('/checkcasenull')
def check_case_null():
    return render_template('checkcase.html')

@app.route('/edit_page')
def editPage():
    cla = USERNAME
    return render_template('edit.html', user_name=cla)

@app.route('/update_page', methods=["POST", "GET"])
def saveEditPage():
    name = request.form.get("name")
    phone = request.form.get("phone")
    user_data = {
                'Name': name,
                'Phone_Number': phone
    }
    db_data.child("users").child(USERNAME).update( user_data)
    cla = USERNAME
    return render_template('edit.html',
                           user_name=cla)
    
@app.route('/main2')
def home_after_login():
    cla = USERNAME
    return render_template('main2.html',
                           user_name=cla)

@app.route('/signin')
def sign_in():
    return render_template('signin.html')

@app.route('/check_case', methods=["POST", "GET"])
def check():
    case_name = request.form.get("Casename")
    image = request.files["Image"]
    Image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    eye, face = imageProcessing.__init__(Image)#changed
    cases = [eye, face]
    classi = classifier.predict([cases])
    if classi == 1:
        cla = 'Has Jaundice'
        TcB = 1
    else:
        cla = 'Does not Have Jaundice'
        TcB = 0
    case_data = {
        'UserName': USERNAME, #changed
        'Eye_Rank': eye,
        'Face_Rank': face,
        'Result': TcB,
        'AI_Mark': 1
    }
    db_data.child("users").child(USERNAME).child("Cases").child(case_name).set(case_data)
    user = USERNAME
    return render_template('result2.html', prediction_text='Patient {}'.format(cla),
                           user_name=user)

@app.route('/CheckNull', methods=["POST", "GET"])
def check_casenull():
    case_name = request.form.get("CaesName")
    image = request.files["Image"]
    Image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)#added and changed
    eye , face = imageProcessing.__init__(Image) #changed
    cases = [eye, face]
    classi = classifier.predict([cases])
    if classi == 1:
        cla = 'Has Jaundice'
        TcB = 1
    else:
        cla = 'Does not Have Jaundice'
        TcB = 0
    case_data = {
        'Eye_Rank': eye,
        'Face_Rank': face,
        'Result': TcB,
        'AI_Mark': 1
    }
    db_data.child("AnounumusCases").child(case_name).set(case_data) 
    return render_template('result.html',
                           prediction_text='Patient {}'.format(cla))

@app.route('/entercase')
def enter_case():
    cla= USERNAME
    print(cla)
    return render_template('entercase2.html',
                           user_name=cla)

@app.route('/save', methods=["POST"])
def save_case():
    case_name = request.form.get("CaesName")
    image = request.files["Image"]
    Image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    TcBC = request.form.get("check-jaundice")
    if TcBC == 0: TcB = 0
    else: TcB = 0
    eye, face = imageProcessing.__init__(Image)
    case_data = {
        'UserName': USERNAME,
        'Eye_Rank': eye,
        'Face_Rank': face,
        'Result': TcB,
        'AI_Mark': 0
    }
    db_data.child("users").child(USERNAME).child("Cases").child(case_name).set(case_data)
    cla = USERNAME
    return render_template('main2.html',
                           user_name=cla)



@app.route('/subuser', methods=["POST", "GET"])
def signin():
    password = request.form.get("password")
    name = request.form.get("name")
    username = request.form.get("username")
    email = request.form.get("email")
    phone = request.form.get("phone")
    try:
        db_auth.create_user_with_email_and_password(email, password)
        try:
            user_data = {
                'Name': name,
                'Email': email,
                'Phone_Number': phone
            }
            db_data.child("users").child(username).set( user_data)
            global USERNAME 
            USERNAME = username
            return render_template('main2.html',
                           user_name=username)
        except:
            # add vat to the new temp
            exception = "User Name already exists"
            return render_template('signinerror.html',
                                   prediction_text='Error {}'.format(exception))
    except:
        # add vat to the new temp
        exception = "Email already exists"
        return render_template('signinerror.html',
                               prediction_text='Error {}'.format(exception))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/logincheck", methods=["POST", "GET"])
def login_handler():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
   
    try: 
        db_auth.sign_in_with_email_and_password(email,password)
        global USERNAME 
        USERNAME = username
        return render_template('main2.html',
                           user_name=username)
    except:
        # dont forget to add a var and put it into the new temp 
        exception = "Invalid Email Or Password"
        return render_template('loginerror.html', 
                               prediction_text='{}'.format(exception))

@app.route('/logout')
def logout():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True)
