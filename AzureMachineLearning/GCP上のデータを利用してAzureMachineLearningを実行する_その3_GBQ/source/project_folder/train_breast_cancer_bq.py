
# ライブラリのインポート

import argparse
import os
from datetime import datetime

import numpy as np
import pandas as pd
import sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn import model_selection 
from sklearn.ensemble import RandomForestClassifier
seed = 0

from google.cloud import bigquery

import joblib

from azureml.core.run import Run
run = Run.get_context()

print('pandas version: ', pd.__version__)
print('sklearn version: ', sklearn.__version__)
print('joblib version: ', joblib.__version__)
print('bigquery version: ', bigquery.__version__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kernel', type=str, default='random_forest', help='Kernel type to be used in the algorithm')
    parser.add_argument('--penalty', type=float, default=1.0, help='Penalty parameter of the error term')
    parser.add_argument('--credentail_path_arg', type=str, default='credentail_path', help='Google credential json file path')
    parser.add_argument('--sql_arg', type=str, default='sql', help='sql query')
    
    args = parser.parse_args()
    run.log('Kernel type', np.str(args.kernel))
    run.log('Penalty', np.float(args.penalty))
    
    # data = load_breast_cancer() # loading the dataset

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.credentail_path_arg
    
    client = bigquery.Client()
    bigquery_data = client.query(args.sql_arg)
    data = bigquery_data.to_dataframe()

    X = data.iloc[:,:-1] # 学習とテストデータ作成
    y = data.iloc[:,-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)
    kfold = model_selection.KFold(n_splits = 5)
    scores = {}

    rfc_clf = RandomForestClassifier(max_depth=5, random_state=seed) #ランダムフォレスト
    rfc_clf.fit(X_train, y_train)
    
    results = model_selection.cross_val_score(rfc_clf, X_test, y_test, cv = kfold) # 結果作成
    scores[('Random Forest', 'train_score')] = results.mean()
    scores[('Random Forest', 'test_score')] = rfc_clf.score(X_test, y_test)
    print(scores)
    run.log('train_accuracy', scores[('Random Forest', 'train_score')])
    run.log('test_accuracy', scores[('Random Forest', 'test_score')])
    
    os.makedirs('outputs', exist_ok=True) # モデル保存
    joblib.dump(rfc_clf, 'outputs/model.joblib')

if __name__ == '__main__':
    main()

