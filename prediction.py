import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.inspection import permutation_importance
import preprocessing

songs, train_set, test_set = preprocessing.preprocess_data('songs.csv')

def visualize_data(model, X_test, y_test, model_name, target_col):
  """
  Visualizes the performance and feature importance of a given model.

  Args:
    model: The trained machine learning model.
    X_test: The test data.
    y_test: The true labels for the test data.
    model_name: The name of the model (e.g., 'Random Forest').
    target_col: The name of the target column.

  """
  # Feature Importance
  if model_name in ['Random Forest', 'Gradient Boosting']:
      importances = model.feature_importances_
      features = X_test.columns
      importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
      importance_df = importance_df.sort_values(by='Importance', ascending=False)
      plt.figure(figsize=(10, 6))
      sns.barplot(x='Importance', y='Feature', data=importance_df)
      plt.title(f'{model_name} Feature Importance for {target_col}')
      plt.show()
  elif model_name in ['SVM', 'KNN']:
      # Permutation importance for models without built-in feature importance
      result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
      importances = result.importances_mean
      features = X_test.columns
      importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
      importance_df = importance_df.sort_values(by='Importance', ascending=False)
      plt.figure(figsize=(10, 6))
      sns.barplot(x='Importance', y='Feature', data=importance_df)
      plt.title(f'{model_name} Feature Importance (Permutation) for {target_col}')
      plt.show()

# Random Forest Classifier
def RF_model(X_train, X_test, y_train, y_test):
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)
    return rf_model

# Support Vector Machine
def SVM_model(X_train, X_test, y_train, y_test):
    svm = SVC(kernel='linear', C=1)
    svm.fit(X_train, y_train)
    y_pred = svm.predict(X_test)
    return svm

# K-nearest neighbours
def KNN_model(X_train, X_test, y_train, y_test):
  KNN_model = KNeighborsClassifier(n_neighbors=5)
  KNN_model.fit(X_train, y_train)
  y_pred = KNN_model.predict(X_test)
  return KNN_model

def GBT_model(X_train, X_test, y_train, y_test):
  gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
  gb_model.fit(X_train, y_train)
  y_pred = gb_model.predict(X_test)
  return gb_model

# Features (X) - Exclude 'track_id', 'artist', 'title', 'release' and all target genre columns
feature_cols = [col for col in songs.columns if col not in ['track_id', 'artist', 'title', 'release'] and not col.startswith('genre_')]
X = songs[feature_cols]

# Iterate through genre columns for target (Y)
for target_col in [col for col in songs.columns if col.startswith('genre_')]:
    Y = songs[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    rf_model = RF_model(X_train, X_test, y_train, y_test)
    visualize_data(rf_model, X_test, y_test, 'Random Forest', target_col)

for target_col in [col for col in songs.columns if col.startswith('genre_')]:
  Y = songs[target_col]
  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
  svm = SVM_model(X_train, X_test, y_train, y_test)
  visualize_data(svm, X_test, y_test, 'SVM', target_col)

for target_col in [col for col in songs.columns if col.startswith('genre_')]:
  Y = songs[target_col]
  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
  knn_model = KNN_model(X_train, X_test, y_train, y_test)
  visualize_data(knn_model, X_test, y_test, 'KNN', target_col)

for target_col in [col for col in songs.columns if col.startswith('genre_')]:
  Y = songs[target_col]
  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
  gb_model = GBT_model(X_train, X_test, y_train, y_test)
  visualize_data(gb_model, X_test, y_test, 'Gradient Boosting', target_col)

