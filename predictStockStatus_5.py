import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_validate
from sklearn.utils import shuffle

#folder and file details
featuresFldr='twFeaturesAndCls'
featuresFn="stockpredict.txt"
#open the file containing the features and classes
fileFeas = open(featuresFldr+'/'+featuresFn, 'r',encoding="utf-8")
#make a vector of features and class
vector = np.loadtxt(fileFeas,dtype=float, delimiter=',')
#seperate features and targe classes
features = np.array(vector[:,0:-1], dtype='float')
target = vector[:,-1]

#perform the the normalization of features
normlzdFeas=np.zeros((features.shape[0],4))
normlzdFeas[:,0]=features[:,0]/(1+features[:,3])
normlzdFeas[:,1]=features[:,1]/(1+features[:,3])
normlzdFeas[:,2]=features[:,0]/(1+features[:,3]-features[:,2])
normlzdFeas[:,3]=features[:,1]/(1+features[:,3]-features[:,2])

#classifier input is X and output is y
X = np.array(normlzdFeas)
y = np.array(target)
X,y=shuffle(X,y)
clf=svm.SVC(C=0.1, tol=0.001, max_iter=100, random_state=1, verbose=1)
scoring = ['accuracy','precision_macro', 'recall_macro']
scores = cross_validate(clf, X, y, scoring=scoring,cv=5, return_train_score=False)
print(scores.keys())
print(scores['test_accuracy'])

fileFeas.close()