# Create an basic Flask app
from flask import Flask, render_template, request
import json

app = Flask(__name__)

currentQuiz = None

data_file = open("data.json", "r", encoding="utf-8")
data = json.load(data_file)
data_file.close()

answer_file = open("finalAnswers.json", "r", encoding="utf-8")
finalAnswers = json.load(answer_file)
answer_file.close()

@app.route("/")
def index():
    global currentQuiz
    currentQuiz = None
    return render_template("index.html", buttonText="開始作答")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        global currentQuiz
        print(currentQuiz)
        if currentQuiz is None:
            currentQuiz = 0
            currentQuestion = data[currentQuiz]["question"]
            print(currentQuestion)
            options = ""
            for idx, option in enumerate(data[currentQuiz]["answers"]):
                options += "<input name='options' type='radio' value='" 
                options += str(idx)
                options += "'>"
                options += "<label>"
                options += option[0]
                options += "</label><br><br>"
            return render_template("index.html", question=currentQuestion, options=options, buttonText="下一題")
        else:
            user_anser = request.form["options"]
            print(user_anser)
            if isinstance(data[currentQuiz]["answers"][int(user_anser)][1], int):
                currentQuiz = data[currentQuiz]["answers"][int(user_anser)][1] - 1
                currentQuestion = data[currentQuiz]["question"]
                print(currentQuestion)
                options = ""
                for idx, option in enumerate(data[currentQuiz]["answers"]):
                    options += "<input name='options' type='radio' value='" 
                    options += str(idx)
                    options += "'>"
                    options += "<label>"
                    options += option[0]
                    options += "</label><br><br>"
                return render_template("index.html", question=currentQuestion, options=options, buttonText="下一題")
            else:
                finalAnswerTitle = finalAnswers[data[currentQuiz]["answers"][int(user_anser)][1]][0]
                finalAnswerContent = finalAnswers[data[currentQuiz]["answers"][int(user_anser)][1]][1]
                finalAnswerContent += "<br><br>"
                currentQuiz = None
                return render_template("index.html", question=finalAnswerTitle,options = finalAnswerContent, buttonText="重新作答")
    return render_template("index.html")
