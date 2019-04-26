from flask import Flask, render_template, url_for, request, jsonify

from papybotapp.wiki_api import main_func


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/parser/', methods=["POST"])
def test():
    if request.method == "POST":
        print(request.form["query"])
        results = main_func(request.form["query"])
        # return f'{results["address"]}, {results["coords"]}, {results["url"]}, {results["content"]}'
        return jsonify(results)

    return "Error in test() views.py"


if __name__ == "__main__":
    app.run()
