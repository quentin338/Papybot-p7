from flask import Flask, render_template, url_for, request, jsonify

from papybotapp.wiki_api import main_func
from papybotapp.google_maps.CONSTANTS import GMAPS_API_KEY


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", api_key=GMAPS_API_KEY)


@app.route('/test')
def test():
    return render_template("test.html", api_key=GMAPS_API_KEY)


@app.route('/parser', methods=["POST"])
def parser():
    if request.method == "POST":
        results = main_func(str(request.data))

        if None in results.values():
            return ""
        # results = {
        #     'address': "10, rue des artistes",
        #     'coords': (10, 10),
        #     'url': "https://www.whatismyip.com",
        #     'content': "Constructed from 1887 to 1889 as the entrance to the 1889 World's Fair, it was initially criticised "
        #                "by some of France's leading artists and intellectuals for its design, but it has become a global cultural "
        #                "icon of France and one of the most recognisable structures in the world.[3] The Eiffel Tower is the most-visited "
        #                "paid monument in the world; 6.91 million people ascended it in 2015."
        #                "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest "
        #                "structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, "
        #                "the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title "
        #                "it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure"
        #                " to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957,"
        #                " it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is "
        #                "the second tallest free-standing structure in France after the Millau Viaduct.",
        #     'bot_response': "La réponse de papybot !"
        # }
        return jsonify(results)

    return "Error in test() views.py"


if __name__ == "__main__":
    app.run()
