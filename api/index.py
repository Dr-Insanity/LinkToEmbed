from flask import Flask, render_template, send_from_directory, request
import urllib.parse

app = Flask(__name__)

@app.route('/embed')
def embed():
    base_url = "https://discordembeds.vercel.app/embed?"
    
    slots = [
        "title",
        "description",
        "color",
    ]

    queries_to_metas = {
        "title": "title",
        "description": "description",
        "color": "theme-color",
    }

    query = {
        queries_to_metas["title"]: "",
        queries_to_metas["description"]: "",
        queries_to_metas["color"]: "",
    }

    # Process query parameters provided in the request
    for embed_feature, embed_value in request.args.items():
        query[embed_feature] = embed_value

    embed = "<head>"
    for key, value in query.items():
        embed += f"<meta name={key} content={value}>"
    embed += "</head>"

    # Build the final URL, including only provided parameters
    embed_url = f"{base_url}{urllib.parse.urlencode(query)}"

    return embed

if __name__ == '__main__':
    app.run()