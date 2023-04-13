import os
from flask import Flask ,request, render_template
import numpy as np
import pandas as pd 
from sklearn.preprocessing import StandardScaler
from insurence_premium.pipeline.prediction_pipeline import CustomData ,PredictPipeline

app = Flask(__name__)

#route for home page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def prediction_data():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            age=request.form.get('age'),
            sex=request.form.get('sex'),
            bmi=request.form.get('bmi'), 
            children=request.form.get('children'),
            smoker=request.form.get('smoker'),
            region=request.form.get('region')
            )
        pred_df=data.get_data_as_frame()
        print(pred_df)
        prediction_pipeline=PredictPipeline()
        results=prediction_pipeline.predict(pred_df)
        return render_template('home.html' ,results=results[0]
        )

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    
    app.run(debug=True)