import pandas as pd
from imblearn.under_sampling import NearMiss
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

#---------------Preprocess Data------------------------------------------------
dataset = pd.read_csv('Strokesdataset_Harvard.csv')
dataset = dataset.drop('id',axis = 1)
DataPrep = dataset.dropna()
#print("gender: ",dataset['gender'].dtypes)
#print("age: ",dataset['age'].dtypes)
#print("hypertension: ",dataset['hypertension'].dtypes)
#print("heart_disease: ",dataset['heart_disease'].dtypes)
#print("work_type: ",dataset['work_type'].dtypes)
#print("Residence_type: ",dataset['Residence_type'].dtypes)
#print("ever_married: ",dataset['ever_married'].dtypes)
#print("avg_glucose_level: ",dataset['avg_glucose_level'].dtypes)
#print("bmi: ",dataset['bmi'].dtypes)
#print("smoking_status: ",dataset['smoking_status'].dtypes)

Cols = ['gender','ever_married','work_type','Residence_type','smoking_status']
Columns = ['gender','age','hypertension','heart_disease','ever_married','work_type','Residence_type','avg_glucose_level','bmi','smoking_status','stroke']
DataPrep[Cols] = DataPrep[Cols].astype('category')
for Columns in Cols:
   DataPrep[Columns] = DataPrep[Columns].cat.codes
   
DataPrep = pd.DataFrame(scaler.fit_transform(DataPrep), columns=DataPrep.columns)

X = DataPrep.drop('stroke',axis = 1)
Y = DataPrep['stroke'] # select only the stroke
nm = NearMiss()
X_res, Y_res =nm.fit_resample(X,Y)

x2_train, x2_test, y2_train, y2_test = train_test_split(X_res,Y_res, test_size=0.2,random_state =1234, stratify= Y_res)
rfc = RandomForestClassifier(
         n_estimators=200,
         max_depth=10,
         min_samples_split=4,
         min_samples_leaf=2,
         max_features= None,
         random_state=1,
         n_jobs=-1
)
rfc.fit(x2_train, y2_train)