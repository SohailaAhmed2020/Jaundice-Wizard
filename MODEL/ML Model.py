import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc, mean_absolute_error, mean_squared_error, r2_score
import pickle


#Load the data
data = pd.read_csv("/media/mina/Mina M. Atalla/Projects/Web_App/WEB_APP/MODEL/DataSet.csv")
x = data.drop(['Jaundice'], axis=1)
y = data['Jaundice']

#Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(x_train)
X_test_scaled = scaler.transform(x_test)

#Train the model
classifier = GaussianNB()
classifier.fit(X_train_scaled, y_train)

#Save the trained model
pickle.dump(classifier, open('model.pkl', 'wb'))

#Make predictions on the test set
y_pred = classifier.predict(X_test_scaled)

#Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
confusion = confusion_matrix(y_test, y_pred)
fpr, tpr, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(fpr, tpr)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

#Print the evaluation metrics
print("Accuracy:", accuracy*100)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:")
print(confusion)
print("ROC AUC Score:", roc_auc)
print("Mean Absolute Error:", mae)
print("Root Mean Squared Error:", mse)
print("R-Squared:", r2)