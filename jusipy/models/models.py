from pandas.tools.plotting import parallel_coordinates
import pandas as pd
from sklearn.metrics import jaccard_similarity_score
from sklearn import metrics
import pickle
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import os
import eli5
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.svm import SVR
#import xgboost as xgb

random_state = 100



class Models:

    """
    Class to evaluate, train and predict:
    Main functions:
        -evaluate : Run crossvalidation on the classifiers
        -fit_model: fit the models with all the data
        -make_predictions: predict for given points
    Algorithms:
    -svm
    -svr
    -rf
    -logistic
    """
    def __init__(self, data_df, label_df):
        """
        Import data and labels files

        """
        #data_file = '%s/data/initial_features.pkl' % dir_path
        #labels_file = '%s/data/initial_labels.pkl' % dir_path
        #if not os.path.exists(data_file):
        #    print("export data file - it does NOT exist")

        #self._data = pickle.load( open( "data/initial_features.pkl", "rb" ))
        #self._labels = pickle.load(open("data/initial_labels.pkl", "rb"))
        self._data = data_df
        self._labels = label_df
        self._model = None
        self._m_name = None
        self._models = {}


    def evaluate(self):

        self._m_name = "Random Forest"
        self._model = RandomForestClassifier(n_estimators=10 ,
                                min_samples_split= 11,
                                min_samples_leaf=17,
                                bootstrap = True,
                                criterion = 'entropy',
                                max_depth = 11,
                                max_features = 11,
                                n_jobs=-1,
                                random_state=100)
        self.make_and_plot_AUROC(self._model, self._data, self._labels, 10)

        self._m_name = "SVM Linear"
        self._model = svm.SVC(kernel='linear', probability=True,random_state=random_state)
        self.make_and_plot_AUROC(self._model, self._data, self._labels, 10)

        self._m_name = "Logistic regression"
        self._model = LogisticRegression(random_state=random_state, solver='lbfgs', multi_class='multinomial')
        self.make_and_plot_AUROC(self._model, self._data, self._labels, 10)

        #self._m_name = "XGboost"
        #self._model = xgb.XGBClassifier(n_estimators=10, objective="binary:logistic")
        #self.make_and_plot_AUROC(self._model, self._data, self._labels, 10)



    def fit(self, clf_list):

        for given_model in clf_list:
            if given_model == 'rf':
        #self._model = RandomForestClassifier(n_estimators=10)
                self._model = RandomForestClassifier(n_estimators=10 ,
                                        min_samples_split= 11,
                                        min_samples_leaf=17,
                                        bootstrap = True,
                                        criterion = 'entropy',
                                        max_depth = 11,
                                        max_features = 11,
                                        n_jobs=-1,
                                        random_state=random_state)

                fitmodel = self._model.fit(self._data, np.ravel(self._labels))
                self._models['rf'] = fitmodel
                print('train accuracy for RF: '+str(jaccard_similarity_score(self._model.predict(self._data), self._labels)))

        #save rf model
        #filename = "models/rf_model.sav"
        #pickle.dump(self._model, open(filename, 'wb'))

            if given_model == 'svm':

                self._model = svm.SVC(kernel='linear', probability=True,random_state=random_state)
                fitmodel = self._model.fit(self._data, np.ravel(self._labels))
                self._models['svm'] = fitmodel
                print('train accuracy for linear SVM: '+str(jaccard_similarity_score(self._model.predict(self._data), self._labels)))

                #save svm linear model
                #filename = "models/svm_linear_model.sav"
                #pickle.dump(self._model, open(filename, 'wb'))

            if given_model == 'lr':
                self._model = LogisticRegression(random_state=random_state, solver='lbfgs', multi_class='multinomial')
                fitmodel = self._model.fit(self._data, np.ravel(self._labels))
                self._models['logistic'] = fitmodel
                print('train accuracy for logistic regression: '+str(jaccard_similarity_score(self._model.predict(self._data), self._labels)))

        #save logistic model
        #filename = "models/logistic_model.sav"
        #pickle.dump(self._model, open(filename, 'wb'))

            if given_model == 'svr':

                self._model = SVR(kernel='linear', C=1e3)
                fitmodel = self._model.fit(self._data, np.ravel(self._labels))
                self._models['svr'] = fitmodel
        #self._model.fit(self._data, np.ravel(self._labels))
        #print('train accuracy for SVR: '+str(jaccard_similarity_score(self._model.predict(self._data), self._labels)))

        #save svr model
        #filename = "models/svr_linear_model.sav"
        #pickle.dump(self._model, open(filename, 'wb'))

        #self._model = xgb.XGBClassifier(n_estimators=10, objective="binary:logistic")
        #self._model.fit(self._data, np.ravel(self._labels))
        #print('train accuracy for XGboost: '+str(jaccard_similarity_score(self._model.predict(self._data), self._labels)))

        #save XGboost model
        #filename = "models/xgboost_model.sav"
        #pickle.dump(self._model, open(filename, 'wb'))


    def predicta(self, mdl, data):
        """
        Get the prediction for a whole dataframe,
        choose:
        mdl = "svm"
        mdl = "rf"
        """
        explanation = []
        final_prediction = []
        if mdl == "svm":
            loaded_model = pickle.load(open("models/svm_linear_model.sav", 'rb'))
        elif mdl == "logistic":
            loaded_model = pickle.load(open("models/logistic_model.sav", 'rb'))
        elif mdl == "rf":
            loaded_model = pickle.load(open("models/rf_model.sav", 'rb'))
        elif mdl == "svr":
            loaded_model = pickle.load(open("models/svr_linear_model.sav", 'rb'))

        if mdl == 'svr':
            ypred = pd.DataFrame({'predict_dataframe': pd.Series(loaded_model.predict(data))})
        else:
            ypred = pd.DataFrame({'predicted_probability': pd.Series(loaded_model.predict_proba(data)[:, 1]),
                                      'predicted_class': pd.Series(loaded_model.predict(data))})
        return(ypred)



    def predictb(self, mdl, data):
        for model in self._models:
            if model == 'svr':
                ypred = pd.DataFrame({'predict_dataframe': pd.Series(model.predict(data))})
            else:
                ypred = pd.DataFrame({'predicted_probability': pd.Series(model.predict_proba(data)[:, 1]),
                                      'predicted_class': pd.Series(loaded_model.predict(data))})
                feats = eli5.explain_prediction_df(model, data, feature_names=list(self._data))
            return(ypred)


    def global_feautures_c(self, data):
        loaded_model1 = pickle.load(open("models/svm_linear_model.sav", 'rb'))
        loaded_model2 = pickle.load(open("models/logistic_model.sav", 'rb'))
        loaded_model3 = pickle.load(open("models/rf_model.sav", 'rb'))
        loaded_model4 = pickle.load(open("models/svr_linear_model.sav", 'rb'))

        self._models['logistic'] = loaded_model2
        self._models['svm'] = loaded_model1
        self._models['rf'] = loaded_model3
        self._models['svr'] = loaded_model4
        self._data = data

        return self.global_feautures_b(data)



    def global_feautures_b(self, data):
        #data = self._data
        final = pd.DataFrame.from_dict({'feature' : list(data.columns) + ['<BIAS>']})
        for model in self._models:
            #print(model)
            #print(self._model[str(model)
            final_features = eli5.explain_weights_df(self._models[str(model)], feature_names= list(data))
            final_features = final_features[['feature','weight']].set_index('feature')
            final_features = final_features.rename(columns={'weight':model})
            final_features.reset_index(drop=True, inplace=True)
            final = final.join(final_features)
        #efor

        return(final)


    def predict_proba(self, data):
        ypreds = {}
        for model_name, model in self._models.items():
            if model_name == 'svr':
                ypreds[model_name] = model.predict(data)
            else:
                ypreds[model_name] = model.predict_proba(data)[:, 1]
            #fi
        #efor
        return pd.DataFrame.from_dict(ypreds)
    #edef



    def make_and_plot_AUROC(self,classifier, X, y, n_folds=10, RF=True, shuffle=True, save_name=''):
        """ Calculates the mean AUROC and plots it."""

        from scipy import interp
        from sklearn.metrics import roc_curve, auc
        from sklearn.model_selection import StratifiedKFold
        # initialize the cross validation object for 10 folds
        cv = StratifiedKFold(n_splits=10, shuffle=shuffle, random_state=0)

        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)

        feature_scores = []

        fig = plt.figure()
        ax = plt.subplot(111)

        fig.set_figwidth(8)
        fig.set_figheight(6)

        i = 0
        X = X.values
        y = y.values

        for train, test in cv.split(X, y):
            if self._m_name == "XGboost":
                # prep the data
                data_train = xgb.DMatrix(X[train], label=y[train])
                data_test = xgb.DMatrix(X[test], label=y[test])
            probas_ = classifier.fit(X[train], np.ravel(y[train])).predict_proba(X[test])
            # Compute ROC curve and area the curve
            fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            plt.plot(fpr, tpr, lw=1, alpha=0.3,
                     label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))

            i += 1
        plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
                 label='Chance', alpha=.8)

        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        plt.plot(mean_fpr, mean_tpr, color='b',
                 label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
                 lw=2, alpha=.8)

        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                         label=r'$\pm$ 1 std. dev.')

        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic of '+self._m_name)
        plt.legend(loc="lower right")
        plt.show()
