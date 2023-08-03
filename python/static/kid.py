import numpy as np 
import pandas as pd
import os, sys
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report,accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from scipy.stats import norm
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.linear_model import SGDClassifier 
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier 
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score,recall_score,precision_score,confusion_matrix,f1_score,roc_auc_score,log_loss
from sklearn.ensemble import VotingClassifier
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV 
from sklearn.linear_model import LogisticRegression
import pickle


#loading dataset
dataset = pd.read_csv('/home/murali/Downloads/kid.csv')
dataset.head(n=10)
print(dataset.describe())
dataset.shape

print(dataset.isnull().sum())


#replace
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy = 'most_frequent')

dataset_imputed = pd.DataFrame(imputer.fit_transform(dataset))
dataset_imputed.columns=dataset.columns
dataset_imputed

print(dataset_imputed.isnull().sum())
print(dataset_imputed["rc"].mode())
print(dataset_imputed["wc"].mode())
print(dataset_imputed["pcv"].mode())
dataset_imputed["classification"]=dataset_imputed["classification"].apply(lambda x:'ckd' if x=="ckd\t" else x)
dataset_imputed["cad"]=dataset_imputed["cad"].apply(lambda x:'no' if x=="\tno" else x)
dataset_imputed["dm"]=dataset_imputed["dm"].apply(lambda x:'no' if x=="\tno" else x)
dataset_imputed["dm"]=dataset_imputed["dm"].apply(lambda x:'yes' if x=="\tyes" else x)
dataset_imputed["dm"]=dataset_imputed["dm"].apply(lambda x:'yes' if x==" yes" else x)
dataset_imputed["rc"]=dataset_imputed["rc"].apply(lambda x:'5.2' if x=="\t?" else x)

dataset_imputed["wc"]=dataset_imputed["wc"].apply(lambda x:'9800' if x=='\t8400' else x)
dataset_imputed["wc"]=dataset_imputed["wc"].apply(lambda x:'6200' if x=='\t6200' else x)
dataset_imputed["wc"]=dataset_imputed["wc"].apply(lambda x:'9800' if x=='\t?' else x)

dataset_imputed["pcv"]=dataset_imputed["wc"].apply(lambda x:'41' if x=='\t?' else x)
dataset_imputed["wc"]=dataset_imputed["wc"].apply(lambda x:'43' if x=='\t43' else x)
#find unique value
for i in dataset_imputed.columns:
    print(i)
    print()
    print(set(dataset_imputed[i].tolist()))
    print()
    
    #label imbalance
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    temp=dataset_imputed["classification"].value_counts()
    temp_dataset = pd.DataFrame({'classification': temp.index,'values': temp.values})
    print(sns.barplot(x='classification',y="values",data=temp_dataset))
    dataset.dtypes
    dataset_imputed.dtypes
    for i in dataset.select_dtypes(exclude=["object"]).columns:
        dataset_imputed[i]=dataset_imputed[i].apply(lambda x: float(x))
        
        dataset_imputed.dtypes
        sns.pairplot(dataset_imputed)
        
        
        #find distribution of data
        
        def distplots(col):
            sns.distplot(dataset[col])
            plt.show()
            
        for i in list(dataset_imputed.select_dtypes(exclude=["object"]).columns)[1:]:
                distplots(i)
                
                #find and remove outliers
        def boxplots(col):
            sns.boxplot(dataset[col])
            plt.show()
            
        for i in list(dataset_imputed.select_dtypes(exclude=["object"]).columns)[1:]:
            boxplots(i)
                
        #label encoding to convert categoriacl values to numerical
    
        from sklearn import preprocessing
        dataset_enco=dataset_imputed.apply(preprocessing.LabelEncoder().fit_transform)
        dataset_enco
        
        dataset_enco.to_csv("kidney_disease_pre-processed.csv")
        
        #find correlation
        
        plt.figure(figsize=(20,20))
        corr=dataset_enco.corr()
        sns.heatmap(corr,annot=True)
        
        #ind dep var
    #    x=dataset_enco.drop(["id","classification"],axis=1)
       # y=dataset_enco["classification"]
        
        X_train, X_test, y_train, y_test = train_test_split(dataset_enco.iloc[:,:-1],dataset_enco['classification'], test_size=0.33, random_state=44, stratify= dataset_enco['classification'])
        print(X_train.shape)
        y_train.value_counts()
        rfc = RandomForestClassifier(random_state = 22)
        rfc_fit = rfc.fit(X_train,y_train)
        rfc_pred = rfc_fit.predict(X_test)
        print(confusion_matrix(y_test,rfc_pred))
        print(classification_report(y_test,rfc_pred))
        accuracy_score( y_test, rfc_pred)
        
        knn = KNeighborsClassifier(n_neighbors=1)
        knn.fit(X_train,y_train)
        pred = knn.predict(X_test)
        print(confusion_matrix(y_test,pred))
        print(classification_report(y_test,pred))
        accuracy_score( y_test,pred)

        logmodel = LogisticRegression()
        logmodel.fit(X_train,y_train)
        predictions = logmodel.predict(X_test)
        print(classification_report(y_test,predictions))
        print(confusion_matrix(y_test,predictions))
        accuracy_score( y_test, predictions)
        feature_importances = pd.DataFrame(rfc.fit(X_train,y_train).feature_importances_, index = X_train.columns,
                                   columns=['importance']).sort_values('importance', ascending=False)
        print(feature_importances)
        kidney3 = dataset_enco.drop(columns=['rbc', 'pc', 'sod', 'pot', 'pcv', 'wc', 'rc'])
        kidney3. shape
        kidney3.head()
        X_train, X_test, y_train, y_test = train_test_split(kidney3.iloc[:,:-1], kidney3['classification'],test_size = 0.33, random_state=44,stratify = kidney3['classification'])
      
        print(X_train.shape)
        y_train.value_counts()
        rfc = RandomForestClassifier(random_state = 22)
        rfc_fit = rfc.fit(X_train,y_train)
        rfc_pred = rfc_fit.predict(X_test)
        print(confusion_matrix(y_test,rfc_pred))
        print(classification_report(y_test,rfc_pred))
        accuracy_score( y_test, rfc_pred)
        
        knn = KNeighborsClassifier(n_neighbors=1)
        knn.fit(X_train,y_train)
        pred = knn.predict(X_test)
        print(confusion_matrix(y_test,pred))
        print(classification_report(y_test,pred))
        accuracy_score( y_test,pred)

        logmodel = LogisticRegression()
        logmodel.fit(X_train,y_train)
        predictions = logmodel.predict(X_test)
        print(classification_report(y_test,predictions))
        print(confusion_matrix(y_test,predictions))
        accuracy_score( y_test, predictions)
        
       
    x =kidney3.copy()
    y = x['classification']
    x = x.drop(['classification'],axis=1)
        
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state = 1234)

        
    
        
    sc = StandardScaler()
    x_sm = sc.fit_transform(x_train)
    x_test_sm = sc.transform(x_test)
        
    model1 = RandomForestClassifier()
    model2 = KNeighborsClassifier()
    model3 = SVC()
    model4 = GaussianNB()
    model5 = DecisionTreeClassifier()
    model6 = LogisticRegression()
    model7 = AdaBoostClassifier()
        
    final_model = VotingClassifier(
        
            estimators = [('RFC',model1),('KNC',model2),('SVC',model3),('GNB',model4),('DTC',model5),('LR',model6),('ABC',model7)] , voting = 'hard'
        )
    final_model.fit(x_sm,y_train)
    pred = final_model.predict(x_test_sm)
    print(accuracy_score(y_test,pred))
        


    sv = SVC().fit(x_sm,y_train)
    pickle.dump(sv, open('kid.pkl', 'wb'))
