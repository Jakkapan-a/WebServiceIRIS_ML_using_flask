## The Iris dataset and scikit-learn and using with flask app
This is a example of using the Iris dataset with scikit-learn and using it with a Flask app

## Structure folder
```bash
.
├── model
│   ├── iris_classifier.joblib
│   ├── train.py
├── src
│   ├── app.py
│   ├── templates
│   │    ├── index.html
├── README.md
```

## How to run
1. Clone the repository
```bash
git clone https://github.com/Jakkapan-a/WebServiceIRIS_ML_using_flask.git
```
2. Install the scikit-learn , Flask and mysql-connector-python
```bash 
pip install scikit-learn Flask mysql-connector-python
```
3. Run the train.py
```bash
python model/train.py
```
4. Run the app.py
```bash
python src/app.py
```
5. Open the browser and go to http://localhost:5000

<!-- img -->
<img src="./images/01.png" alt="01" width="200"/>

## Update Save result to MySQL and show in the all_result page

<!-- img -->
<img src="./images/02.png" alt="02" width="200"/>