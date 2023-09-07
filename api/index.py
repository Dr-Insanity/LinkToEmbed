from flask import Flask, render_template, send_from_directory, request
import urllib.parse

app = Flask(__name__)

@app.route('/embed')
def embed():
    base_url = "https://oembed.vercel.app/embed?"
    query = {}
    for embed_feature, embed_value in request.args:
        query[embed_feature] = embed_value

    embed_url = f"{base_url+urllib.parse.urlencode(query)}"

    return f'<iframe width="500" height="300" src="{embed_url}"></iframe>'

if __name__ == '__main__':
    app.run()