import os
import pandas as pd
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sklearn.multiclass import *


app = Flask(__name__)
global Classifier_severity
global Classifier_type
global msg_vectorizer
global causedby1_msg_vectorizer
global causedby2_msg_vectorizer

path = 'data/exception_data.csv'
dataFrame = pd.read_csv(path)

df_master=dataFrame[["Module", "Language","Exception","CausedBy1","CausedBy2"]]
df_lable=dataFrame[["Severity"]]
df_type=dataFrame[["Type"]]
df_message=dataFrame[["Message"]]
df_causedBy1Msg=dataFrame[["CausedBy1Msg"]]
df_causedBy2Msg=dataFrame[["CausedBy2Msg"]]


msg_vectorizer = CountVectorizer(ngram_range=(2, 3))
msg_train_dtm = msg_vectorizer.fit_transform(df_message.Message)
message_trigramed_frame= pd.DataFrame(msg_train_dtm.toarray(),columns=msg_vectorizer.get_feature_names())

causedby1_msg_vectorizer = CountVectorizer(ngram_range=(2, 3))
msg_causedby1_train_dtm = causedby1_msg_vectorizer.fit_transform(df_causedBy1Msg.CausedBy1Msg)
causedby1_msg_trigramed_frame=pd.DataFrame(msg_causedby1_train_dtm.toarray(),columns=causedby1_msg_vectorizer.get_feature_names())

causedby2_msg_vectorizer = CountVectorizer(ngram_range=(2, 3))
msg_causedby2_train_dtm = causedby2_msg_vectorizer.fit_transform(df_causedBy2Msg.CausedBy2Msg)
causedby2_msg_trigramed_frame=pd.DataFrame(msg_causedby2_train_dtm.toarray(),columns=causedby2_msg_vectorizer.get_feature_names())

df1=pd.merge(df_master, message_trigramed_frame, left_index=True, right_index=True)
df2=pd.merge(df1, causedby1_msg_trigramed_frame, left_index=True, right_index=True)
df3=pd.merge(df2, causedby2_msg_trigramed_frame, left_index=True, right_index=True)

#Decision Tree
Classifier_severity = tree.DecisionTreeClassifier()
Classifier_severity.fit(df3, df_lable)

Classifier_type= tree.DecisionTreeClassifier()
Classifier_type.fit(df3, df_type)

#Testing

@app.route('/')
def index():
	return "Exception Prediction API..."
	
@app.route('/predict/severity', methods=['GET'])
def predictSevirity():
    module = request.args.get('module', '')
    language = request.args.get('language', '')
    exception = request.args.get('exception', '')
    causedby1 = request.args.get('causedby1', '')
    causedby2 = request.args.get('causedby2', '')
    message = request.args.get('message', '')
    causedBy1Msg = request.args.get('causedBy1Msg', '')
    causedBy2Msg = request.args.get('causedBy2Msg', '')
	
    serviceError = ''
    severity = ''
    predict = ''

    global Classifier_severity
    global msg_vectorizer
    global causedby1_msg_vectorizer
    global causedby2_msg_vectorizer
	
    try:
        if len(message) > 0:
          exception_df = pd.DataFrame({'Module':[module],'Language':[language],'Exception':[exception],'CausedBy1' : [causedby1],'CausedBy2' : [causedby2],'Message' : [message], 'CausedBy1Msg' : [causedBy1Msg], 'CausedBy2Msg' : [causedBy2Msg]})
          df_master_test=exception_df[["Module", "Language","Exception","CausedBy1","CausedBy2"]]
          df_message_test=exception_df[["Message"]]
          df_causedBy1Msg_test=exception_df[["CausedBy1Msg"]]
          df_causedBy2Msg_test=exception_df[["CausedBy2Msg"]]
		  
          msg_test_dtm = msg_vectorizer.transform(df_message_test.Message)
          msg_test_causedby1_dtm = causedby1_msg_vectorizer.transform(df_causedBy1Msg_test.CausedBy1Msg)
          msg_test_causedby2_dtm = causedby2_msg_vectorizer.transform(df_causedBy2Msg_test.CausedBy2Msg)

          test_msg_trigramed_frame= pd.DataFrame(msg_test_dtm.toarray(),columns=msg_vectorizer.get_feature_names())
          test_causedby1_msg_trigramed_frame=pd.DataFrame(msg_test_causedby1_dtm.toarray(),columns=causedby1_msg_vectorizer.get_feature_names())
          test_causedby2_msg_trigramed_frame=pd.DataFrame(msg_test_causedby2_dtm.toarray(),columns=causedby2_msg_vectorizer.get_feature_names())

          test_df1=pd.merge(df_master_test, test_msg_trigramed_frame, left_index=True, right_index=True)
          test_df2=pd.merge(test_df1, test_causedby1_msg_trigramed_frame, left_index=True, right_index=True)
          test_df3=pd.merge(test_df2, test_causedby2_msg_trigramed_frame, left_index=True, right_index=True)

          predict = Classifier_severity.predict(test_df3)[0]
		  
          if predict == 1:
           severity='Error'
          elif predict== 0:
           severity='Warning'
          
    except BaseException as inst:
        error = str(type(inst).__name__) + ' ' + str(inst)
    return jsonify(message=message,severity=severity, serviceError=serviceError)
	


@app.route('/predict/issueType', methods=['GET'])
def predictIssueType():
    module = request.args.get('module', '')
    language = request.args.get('language', '')
    exception = request.args.get('exception', '')
    causedby1 = request.args.get('causedby1', '')
    causedby2 = request.args.get('causedby2', '')
    message = request.args.get('message', '')
    causedBy1Msg = request.args.get('causedBy1Msg', '')
    causedBy2Msg = request.args.get('causedBy2Msg', '')
	
    serviceError = ''
    issueType = ''
    predict = ''

    global Classifier_type
    global msg_vectorizer
    global causedby1_msg_vectorizer
    global causedby2_msg_vectorizer
	
    try:
        if len(message) > 0:
          exception_df = pd.DataFrame({'Module':[module],'Language':[language],'Exception':[exception],'CausedBy1' : [causedby1],'CausedBy2' : [causedby2],'Message' : [message], 'CausedBy1Msg' : [causedBy1Msg], 'CausedBy2Msg' : [causedBy2Msg]})
          df_master_test=exception_df[["Module", "Language","Exception","CausedBy1","CausedBy2"]]
          df_message_test=exception_df[["Message"]]
          df_causedBy1Msg_test=exception_df[["CausedBy1Msg"]]
          df_causedBy2Msg_test=exception_df[["CausedBy2Msg"]]
		  
          msg_test_dtm = msg_vectorizer.transform(df_message_test.Message)
          msg_test_causedby1_dtm = causedby1_msg_vectorizer.transform(df_causedBy1Msg_test.CausedBy1Msg)
          msg_test_causedby2_dtm = causedby2_msg_vectorizer.transform(df_causedBy2Msg_test.CausedBy2Msg)

          test_msg_trigramed_frame= pd.DataFrame(msg_test_dtm.toarray(),columns=msg_vectorizer.get_feature_names())
          test_causedby1_msg_trigramed_frame=pd.DataFrame(msg_test_causedby1_dtm.toarray(),columns=causedby1_msg_vectorizer.get_feature_names())
          test_causedby2_msg_trigramed_frame=pd.DataFrame(msg_test_causedby2_dtm.toarray(),columns=causedby2_msg_vectorizer.get_feature_names())

          test_df1=pd.merge(df_master_test, test_msg_trigramed_frame, left_index=True, right_index=True)
          test_df2=pd.merge(test_df1, test_causedby1_msg_trigramed_frame, left_index=True, right_index=True)
          test_df3=pd.merge(test_df2, test_causedby2_msg_trigramed_frame, left_index=True, right_index=True)

          predict = Classifier_type.predict(test_df3)[0]
          
          if predict == 1:
           issueType='Development'
          elif predict== 2:
           issueType='Data Quality'
          elif predict== 3:
           issueType='Configuration'
          
    except BaseException as inst:
        serviceError = str(type(inst).__name__) + ' ' + str(inst)
    return jsonify(message=message,issueType=issueType, serviceError=serviceError)

	

if __name__ == '__main__':
    port = int(os.environ.get('PORT',8080))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)
