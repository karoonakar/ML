import pandas as pd
from sklearn import tree
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

path = 'data/exception_data.csv'
dataFrame = pd.read_csv(path)


df_master=dataFrame[["Module", "Language","Exception","CausedBy1","CausedBy2"]]
df_lable=dataFrame[["Severity"]]
df_message=dataFrame[["Message"]]
df_causedBy1Msg=dataFrame[["CausedBy1Msg"]]
df_causedBy2Msg=dataFrame[["CausedBy2Msg"]]

vect_msg = CountVectorizer(ngram_range=(2, 3))
msg_train_dtm = vect_msg.fit_transform(df_message.Message)
message_trigramed_frame= pd.DataFrame(msg_train_dtm.toarray(),columns=vect_msg.get_feature_names())

vect_causedby1_msg = CountVectorizer(ngram_range=(2, 3))
msg_causedby1_train_dtm = vect_causedby1_msg.fit_transform(df_causedBy1Msg.CausedBy1Msg)
causedby1_msg_trigramed_frame=pd.DataFrame(msg_causedby1_train_dtm.toarray(),columns=vect_causedby1_msg.get_feature_names())

vect_causedby2_msg = CountVectorizer(ngram_range=(2, 3))
msg_causedby2_train_dtm = vect_causedby2_msg.fit_transform(df_causedBy2Msg.CausedBy2Msg)
causedby2_msg_trigramed_frame=pd.DataFrame(msg_causedby2_train_dtm.toarray(),columns=vect_causedby2_msg.get_feature_names())


df1=pd.merge(df_master, message_trigramed_frame, left_index=True, right_index=True)
df2=pd.merge(df1, causedby1_msg_trigramed_frame, left_index=True, right_index=True)
df3=pd.merge(df2, causedby2_msg_trigramed_frame, left_index=True, right_index=True)

print(df3)
print(df3.shape)
print(df_lable.shape)


#Decision Tree
dtClassifier = tree.DecisionTreeClassifier()
dtClassifier.fit(df3, df_lable)

#Testing
exception_df = pd.DataFrame({'Module':[11],'Language':[100],'Exception':[10019],'CausedBy1' : [0],'CausedBy2' : [0],'Message' : ['could not execute native bulk manipulation query at com.sgcib.mrploader'], 'CausedBy1Msg' : ['NoCausedBy oneMsg'], 'CausedBy2Msg' : ['NoCausedBy twoMsg']})
df_master_test=exception_df[["Module", "Language","Exception","CausedBy1","CausedBy2"]]
df_message_test=exception_df[["Message"]]
df_causedBy1Msg_test=exception_df[["CausedBy1Msg"]]
df_causedBy2Msg_test=exception_df[["CausedBy2Msg"]]

msg_test_dtm = vect_msg.transform(df_message_test.Message)
msg_test_causedby1_dtm = vect_causedby1_msg.transform(df_causedBy1Msg_test.CausedBy1Msg)
msg_test_causedby2_dtm = vect_causedby2_msg.transform(df_causedBy2Msg_test.CausedBy2Msg)

test_msg_trigramed_frame= pd.DataFrame(msg_test_dtm.toarray(),columns=vect_msg.get_feature_names())
test_causedby1_msg_trigramed_frame=pd.DataFrame(msg_test_causedby1_dtm.toarray(),columns=vect_causedby1_msg.get_feature_names())
test_causedby2_msg_trigramed_frame=pd.DataFrame(msg_test_causedby2_dtm.toarray(),columns=vect_causedby2_msg.get_feature_names())

test_df1=pd.merge(df_master_test, test_msg_trigramed_frame, left_index=True, right_index=True)
test_df2=pd.merge(test_df1, test_causedby1_msg_trigramed_frame, left_index=True, right_index=True)
test_df3=pd.merge(test_df2, test_causedby2_msg_trigramed_frame, left_index=True, right_index=True)
print(test_df3)

print(dtClassifier.predict(test_df3))
