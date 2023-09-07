from flask import Flask, render_template, send_from_directory, request
import urllib.parse

app = Flask(__name__)

@app.route('/embed')
def embed():
    base_url = "https://discordembeds.vercel.app/embed?"
    query = {}
    embed = "<head>"
    for embed_feature, embed_value in request.args.items():
        query[embed_feature] = embed_value
        embed += "<meta name={} content={}>".format(embed_feature, embed_value)
    embed += f"""</head>\n<body>\n<p>{query["title"]}</p>\n<p>{query["description"]}</p>\n</body>"""
    embed_url = f"{base_url+urllib.parse.urlencode(query)}"

    return embed

if __name__ == '__main__':
    app.run()