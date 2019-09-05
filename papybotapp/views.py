import os
from flask import Flask, render_template, url_for, request, jsonify

from papybotapp.wiki_api import main_func


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", api_key=os.getenv("API_KEY_FRONT"))


@app.route('/parser', methods=["POST"])
def parser():
    if request.method == "POST":
        results = {
            'address': "10, rue des artistes",
            'coords': (10, 10),
            'url': "https://www.whatismyip.com",
            'content': "It was the first structure"
                       "ial at the top of the tower in 1957,"
                       "ng transmitters, the Eiffel Tower is "
                       "ct.",
            'thumbnail': "/static/img/wiki_logo.jpg",
            'bot_response': "La réponse de papybot !"
        }

        results = main_func(str(request.data))

        return jsonify(results)


if __name__ == "__main__":
    app.run()
