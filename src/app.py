from flask import Flask, request, jsonify, render_template
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load
from sklearn.datasets import load_iris
import mysql.connector

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="iris"
)

# Create table history if not exists
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS history (id INT AUTO_INCREMENT PRIMARY KEY, sepal_length FLOAT, sepal_width FLOAT, petal_length FLOAT, petal_width FLOAT, prediction VARCHAR(255), accuracy FLOAT)")

# Load iris dataset
iris = load_iris()
import os
app = Flask(__name__)

file_path = os.path.join(os.getcwd(),'model/iris_classifier.joblib')
# Debug for run in src folder
if(not os.path.exists(file_path)):
    file_path = file_path.replace('src/','').replace('src\\','')
file_path = file_path.replace('\\','/');


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        print('file path: ', file_path)
        print('load model from: ', load(""+file_path))
        model = load(file_path)
        features = [data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']]
        prediction = model.predict([features])
        # Convert numpy array to list
        prediction = prediction.tolist()
        result = jsonify({
            'input': {
                'sepal_length': data['sepal_length'],
                'sepal_width': data['sepal_width'],
                'petal_length': data['petal_length'],
                'petal_width': data['petal_width']
            },
            'prediction': iris.target_names[prediction[0]],
            'accuracy': model.score(iris.data, iris.target)
        })

        # Save to database
        save_history({
            'sepal_length': data['sepal_length'],
            'sepal_width': data['sepal_width'],
            'petal_length': data['petal_length'],
            'petal_width': data['petal_width'],
            'prediction': iris.target_names[prediction[0]],
            'accuracy': model.score(iris.data, iris.target)
        })

        return result
        
    except Exception as e:
        return jsonify({'error': str(e)})
    return jsonify({'error': 'An error occurred'})


@app.route('/all_result', methods=['GET'])
def all_result():
    try:
        mycursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 100")
        result = mycursor.fetchall()
        results = []
        for row in result:
            results.append({
                'id': row[0],
                'sepal_length': row[1],
                'sepal_width': row[2],
                'petal_length': row[3],
                'petal_width': row[4],
                'prediction': row[5],
                'accuracy': row[6]
            })

        return render_template('all_result.html', results=results)
    except Exception as e:
        return jsonify({'error': str(e)})
    return jsonify({'error': 'An error occurred'})

def save_history(data):
    try:
        sql = "INSERT INTO history (sepal_length, sepal_width, petal_length, petal_width, prediction, accuracy) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width'], data['prediction'], data['accuracy'])
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    except Exception as e:
        print('Error save_history: ', str(e))
        return False

if __name__ == '__main__':
    app.run(debug=True, port=5000)