import os,sys
import certifi
from flask import Flask,redirect,render_template,request,url_for,make_response
ca = certifi.where()
from netwoksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION,DATA_INGESTION_DATABASE
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.pipeline.training_pipeline import TrainingPipeline
from dotenv import load_dotenv
import pandas as pd
from netwoksecurity.utils.main_utils.utils import load_obj
from netwoksecurity.utils.ml_utils.model.estimator import NetworkModel
load_dotenv()
import io,json
url = os.getenv("mongo_db_url")
import pymongo
client = pymongo.MongoClient(url  , tlsCAFile = ca)
database = client[DATA_INGESTION_DATABASE]
collection = database[DATA_INGESTION_COLLECTION]


app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask App"


@app.route('/train')
def train():
    try:
        trainer = TrainingPipeline()
        trainer.run_pipeline()
        return "Trainer Pipeline: Training pipeline finishd execution"
    except Exception as e:
        raise CustomException(e,sys)
    
@app.route("/upload", methods=["GET"])
def upload_form():
    return render_template("upload.html")

@app.route("/predict", methods=["POST"])
def predict_route():
    try:
        if "file" not in request.files:
            return "No file part in request", 400

        uploaded_file = request.files["file"]
        if uploaded_file.filename == "":
            return "No selected file", 400

        df = pd.read_csv(uploaded_file)
        if 'Result' in df.columns:
            df.drop(columns=['Result'], inplace=True)

        preprocessor = load_obj("final_model/preprocessor.pkl")
        final_model = load_obj("final_model/model.pkl")

        network_model = NetworkModel(processor=preprocessor, model=final_model)
        y_pred = network_model.predict(df)

        df["predicted_column"] = y_pred
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)

        table_html = df.to_html(classes="table table-striped", index=False)
        return render_template("table.html", df=df , zip =zip)

    except Exception as e:
        raise CustomException(e, sys)
    
from flask import send_file

@app.route('/download', methods=["GET"])
def download_csv():
    try:
        file_path = "prediction_output/output.csv"
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        raise CustomException(e, sys)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80 , debug=True)