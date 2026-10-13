import pandas as pd
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def formPage():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/ryanchung403/dataset/main/train_data_titanic.csv",
        encoding="cp950",
    )  
    
    # Count Survived vs Not Survived
    survived_count = df['Survived'].value_counts().to_dict()

    # Count Male vs Female
    sex_count = df['Sex'].value_counts().to_dict()

    # Count Embarked: S/C/Q
    embarked_count = df['Embarked'].value_counts().to_dict()

    return render_template('index.html', survived_count=survived_count, sex_count=sex_count, embarked_count=embarked_count)

   
if __name__ == '__main__':
    app.run()
