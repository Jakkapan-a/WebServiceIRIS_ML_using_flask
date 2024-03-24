from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib
import os
# Load the Iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Decision Tree classifier and train it
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Export the trained model to a file
model_filename = 'model/iris_classifier.joblib'
if not os.path.exists('model'):
    model_filename = model_filename.replace('model/', '')



joblib.dump(clf, model_filename)

print(f"Model saved to {model_filename}")