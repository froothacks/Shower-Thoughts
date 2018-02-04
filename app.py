from flask import Flask
from flask import request
import requests


app = Flask(__name__)


@app.route("/")
def get_index():
	return "Hello World"

@app.route("/results")
def get_results():
	
	return "Hello World"


if __name__ == '__main__':
	app.run(debug=True)
