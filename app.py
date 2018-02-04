import markovify
import pickle
from flask import Flask, render_template
from flask import request

with open("data-processing/keywords.dat", "rb") as k:
    keywords = pickle.load(k)

with open("data-processing/lyrics.dat", "rb") as l:
    lyrics = pickle.load(l)
app = Flask(__name__)


def suggest_nextlines(inputText, numberLines):
    outputText = []
    text_model = markovify.Text(inputText)
    count = 0
    while len(outputText) < numberLines:
        v = text_model.make_sentence()
        if v:
            outputText.append(v)
        count += 1
        if count > 1000:
            break
    return outputText


def get_lyrics_to_topic(topic):
    corpus = ""
    if topic in keywords:
        for uid in keywords[topic]:
            corpus += lyrics[uid] + "\n"
    return suggest_nextlines(corpus, 3)


@app.route("/")
def get_index():
    return render_template("index.html")


@app.route("/results")
def get_results():
    result = request.args.get("key")
    lyrics = get_lyrics_to_topic(result)
    return render_template("indexResult.html", result=lyrics)


if __name__ == '__main__':
    app.run(debug=True)
