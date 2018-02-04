from flask import Flask, render_template
from flask import request

app = Flask(__name__)


@app.route("/")
def get_index():
    return render_template("index.html")


@app.route("/results")
def get_results():
    result = request.args.get("key")
    return render_template("indexResult.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)
