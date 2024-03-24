from flask import Flask, request, jsonify, render_template
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load
from sklearn.datasets import load_iris
iris = load_iris()
import os
app = Flask(__name__)

file_path = os.path.join(os.getcwd(),'model/iris_classifier.joblib')
# Debug for run in src folder
if(not os.path.exists(file_path)):
    file_path = file_path.replace('src/','').replace('src\\','')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        model = load(file_path)
        features = [data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']]
        prediction = model.predict([features])
        # Convert numpy array to list
        prediction = prediction.tolist()
        return jsonify({
            'input': {
                'sepal_length': data['sepal_length'],
                'sepal_width': data['sepal_width'],
                'petal_length': data['petal_length'],
                'petal_width': data['petal_width']
            },
            'prediction': iris.target_names[prediction[0]],
            'accuracy': model.score(iris.data, iris.target)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})
    return jsonify({'error': 'An error occurred'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)