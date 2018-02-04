import markovify
import pickle
from flask import Flask, render_template
from flask import request

with open("data-processing/keywords.dat", "rb") as f:
    keywords = pickle.load(f)

with open("data-processing/lyrics.dat", "rb") as f:
    lyrics = pickle.load(f)


app = Flask(__name__)


def suggest_nextlines(inputText, numberLines):
    print("Input text:",inputText)
    outputText = []
    text_model = markovify.NewlineText(inputText)
    count = 0
    while len(outputText) < numberLines:
        v = text_model.make_sentence()
        if v:
            outputText.append(v)
        count += 1
        if count > 1000:
            break
    print ("Output",outputText)
    return outputText


def get_lyrics_to_topic(topics):
    corpus = ""
    for i in topics:
        if i in keywords:
             for uid in keywords[i]:
                corpus += lyrics[uid] + "\n"
    return suggest_nextlines(corpus, 4)


@app.route("/")
def get_index():
    return render_template("index.html")


@app.route("/results")
def get_results():
    result = request.args.get("key")
    topics = [x.strip().lower() for x in result.split(",")]
    print(topics)
    all_lyrics = "<br />".join(get_lyrics_to_topic(topics))
    return render_template("indexResult.html", result=all_lyrics)


if __name__ == '__main__':
    app.run(debug=True)
