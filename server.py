import firestore
from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import json

import socket
import socket
from joblib import load
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
ID_code = ''

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/get_user_information')
def get_users():
    users = []
    # Query the 'User' collection and convert documents to a list of dictionaries
    user_docs = db.collection('User').stream()
    for user in user_docs:
        user_data = user.to_dict()
        users.append(user_data)
    
    # Thay đổi tên tập tin ở đây
    file_name = 'New_User.json'

    with open(file_name, 'w') as json_file:
        json.dump(users, json_file, indent=4)

    # Return the list of users as JSON
    return jsonify({'users': users})

@app.route('/get_json_file',methods = ['POST'])
def get_json_file():
    file_path = 'User.json'
    try:
        # Mở tệp JSON và đọc dữ liệu
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return "File not found"
@app.route('/esp8266', methods = ['POST'])
def esp8266JsonHandler():
    content = request.get_json()
    # collection_name/document_id)
    collection_name = 'User'
    document_id = str(ID_code)
    field_name = 'Blood_Pressure_and_Heart_Rate'
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.update({field_name: content})
    return jsonify(content)

@app.route("/predict", methods = ['POST'])
def submit():
    global ID_code
    if request.method == "POST":
        try:
            request_data = request.get_json()
#--------------------------------------------------------------------------------------------
            Arg1_gender = request_data['arg_1']
            Arg2_age = request_data['arg_2']
            Arg3_hypertension = request_data['arg_3']
            Arg4_heart_disease = request_data['arg_4']
            Arg5_ever_married = request_data['arg_5']
            Arg6_work_type = request_data['arg_6']
            Arg7_Residence_type = request_data['arg_7']
            Arg8_avg_glucose_level = request_data['arg_8']
            Arg9_bmi = request_data['arg_9']
            Arg10_smoking_status = request_data['arg_10']
            ID_code = request_data['arg_11']
#------------------xu ly du lieu----------------------------------------------------------------
            if Arg1_gender == 'Nam' or Arg1_gender == 'nam':
                Arg1_gender = 'Male'
            else:
                Arg1_gender = 'Female'

            if Arg3_hypertension == 'co' or Arg3_hypertension == 'Co' or Arg3_hypertension == 'có' or Arg3_hypertension == 'Có':
                Arg3_hypertension = 1
            else:
                Arg3_hypertension = 0;
            
            if Arg4_heart_disease == 'co' or Arg4_heart_disease == 'Co' or Arg4_heart_disease == 'có' or Arg4_heart_disease == 'Có':
                Arg4_heart_disease = 1
            else:
                Arg4_heart_disease = 0;
            
            if Arg5_ever_married == 'co' or Arg5_ever_married == 'Co' or Arg5_ever_married == 'có' or Arg5_ever_married == 'Có':
                Arg5_ever_married = "Yes"
            else:
                Arg5_ever_married = "No"
            
            if "Chưa từng" in Arg10_smoking_status or "chưa từng" in Arg10_smoking_status:
                Arg10_smoking_status = "never smoked"
            elif "Đã từng" in Arg10_smoking_status or "đã từng" in Arg10_smoking_status:
                Arg10_smoking_status = "formerly smoked"
            else:
                Arg10_smoking_status = "smokes"




#------------------------------------------------------------------------------------------------
            new_data = pd.DataFrame(
                [[Arg1_gender, Arg2_age,Arg3_hypertension,Arg4_heart_disease,Arg5_ever_married,Arg6_work_type,Arg7_Residence_type,Arg8_avg_glucose_level,Arg9_bmi,Arg10_smoking_status, 0]],
                columns=['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type',
                         'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'])
            print(new_data)
            dataframe = pd.read_csv('Strokesdataset_Harvard.csv')
            dataframe = dataframe.drop('id',axis = 1)
            dataframe = pd.concat([new_data, dataframe], ignore_index=True)
            dataframe = dataframe.dropna()            
            Cols = ['gender','ever_married','work_type','Residence_type','smoking_status']
            Columns = ['gender','age','hypertension','heart_disease','ever_married','work_type','Residence_type','avg_glucose_level','bmi','smoking_status','stroke']
            dataframe[Cols] = dataframe[Cols].astype('category')
            for Columns in Cols:
                dataframe[Columns] = dataframe[Columns].cat.codes

            dataframe['age'] = dataframe['age'].astype(float)
            dataframe['bmi'] = dataframe['bmi'].astype(float)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].astype(float)

            dataframe['age'] = dataframe['age'].apply(lambda x: 1 if ((x >= 0) and(x<10)) else x)
            dataframe['age'] = dataframe['age'].apply(lambda x: 2 if ((x >= 10) and(x<20)) else x)
            dataframe['age'] = dataframe['age'].apply(lambda x: 3 if ((x >= 20) and(x<30)) else x)
            dataframe['age'] = dataframe['age'].apply(lambda x: 4 if ((x >= 30) and(x<40)) else x)
            dataframe['age'] = dataframe['age'].apply(lambda x: 5 if ((x >= 40) and(x<50)) else x)
            dataframe['age'] = dataframe['age'].apply(lambda x: 6 if ((x >= 50)  and(x<60)) else x)
            dataframe['age'] = dataframe['age'].apply(lambda x: 7 if ((x >= 60) and(x<70)) else x)
            dataframe['age'] = dataframe['age'].apply(lambda x: 8 if (x >= 70) else x)

            dataframe['bmi'] = dataframe['bmi'].apply(lambda x: 1 if ((x >= 0) and(x<18.5)) else x)
            dataframe['bmi'] = dataframe['bmi'].apply(lambda x: 2 if ((x >= 18.5) and(x<25)) else x)
            dataframe['bmi'] = dataframe['bmi'].apply(lambda x: 3 if ((x >= 25) and(x<30)) else x)
            dataframe['bmi'] = dataframe['bmi'].apply(lambda x: 4 if ((x >= 30) and(x<35)) else x)
            dataframe['bmi'] = dataframe['bmi'].apply(lambda x: 5 if ((x >= 35) and(x<40)) else x)
            dataframe['bmi'] = dataframe['bmi'].apply(lambda x: 6 if ((x >= 40) and(x<50)) else x)
            dataframe['bmi'] = dataframe['bmi'].apply(lambda x: 7 if ((x >= 50) and(x<60)) else x)
            dataframe['bmi'] = dataframe['bmi'].apply(lambda x: 8 if ((x >= 60) and(x<70)) else x)
            dataframe['bmi'] = dataframe['bmi'].apply(lambda x: 9 if (x >= 70) else x)

            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 1 if ((x >= 0) and(x<50)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 2 if ((x >= 50) and(x<80)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 3 if ((x >= 80) and(x<115)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 4 if ((x >= 115) and(x<150)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 5 if ((x >= 150) and(x<180)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 6 if ((x >= 180) and(x<215)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 7 if ((x >= 215) and(x<250)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 8 if ((x >= 250) and(x<280)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 9 if ((x >= 280) and(x<315)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 10 if ((x >= 315) and(x<350)) else x)
            dataframe['avg_glucose_level'] = dataframe['avg_glucose_level'].apply(lambda x: 11 if ((x >= 350) and(x<380)) else x)
           

#            print(dataframe)

#--------------Data Normalization-----------------------------------------------------------------
            scaler = MinMaxScaler()
            dataframe = pd.DataFrame(scaler.fit_transform(dataframe), columns=dataframe.columns)
            dataframe = dataframe.drop('work_type',axis = 1)
            dataframe = dataframe.drop('Residence_type',axis = 1)
            input = dataframe.head(1)
            model =load('model.joblib') 
            input = input.drop('stroke', axis=1)
            print(input)
            Result = model.predict(input)
            if(Result == 0):
                Result = 'Không có nguy cơ đột quỵ'
            else:
                Result = 'có nguy cơ đột quỵ'
            
            print(Result)
            collection_name = 'User'
            document_id = str(ID_code)
            field_name = 'Blood_Pressure_and_Heart_Rate'
            doc_ref = db.collection(collection_name).document(document_id)
            doc_ref.update({field_name: {
            'Huyet ap tam truong': '',
            'Huyet ap tam thu': '',
            'Nhip tim': ''
        }})
            doc_ref.update({'Nguy_co_dot_quy': f'{Result}'})

            return Result
        except json.JSONDecodeError as e:
            return jsonify({'error': f'Lỗi khi giải mã JSON: {e}'})
        except Exception as e:
            return jsonify({'error': f'Có lỗi xảy ra: {e}'})
    else:
        return "Phương thức yêu cầu không hợp lệ"

@app.route('/updateID', methods = ['POST'])
def ID_update():
    global ID_code
    content = request.get_json()
    ID_code = content['ma_nguoi_dung']
    return jsonify(content)

if __name__ == '__main__':
    app.run(debug=True, port=5000)