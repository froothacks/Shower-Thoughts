from flask import Flask, render_template, request
from flask import request

app = Flask(__name__)


@app.route("/")
def get_index():
    return render_template("ShowerThoughts.html")


@app.route("/results")
def get_results():
    result = request.args.get("key")
    return render_template("ShowerThoughtsResult.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)
