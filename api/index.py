from flask import Flask, render_template, send_from_directory, request, send_file
import urllib.parse
import html

app = Flask(__name__, template_folder='../templates')

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

    for embed_feature, embed_value in request.args.items():
        try:
            print("query: %s" % embed_feature)
            print("value: %s" % embed_value)
            query[queries_to_metas[embed_feature]] = embed_value
        except KeyError:
            continue

    embed = "<head>\n   "
    for key, value in query.items():
        embed += f"""<meta name={key} content="{html.escape(value)}">"""
    embed += "</head>"

    # Build the final URL, including only provided parameters
    embed_url = f"{base_url}{urllib.parse.urlencode(query)}"

    return embed

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()