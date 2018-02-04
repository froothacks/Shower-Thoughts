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
    try:
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
        return "<br />".join(outputText)
    except:
        pass


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
    keywords = request.args.get("key")
    topics = [s.strip().lower() for s in keywords.split(",")]
    print(topics)
    result = get_lyrics_to_topic(topics) or "No data"
    return render_template("index.html", keywords=keywords, result=result)


if __name__ == '__main__':
    app.run(debug=True)
