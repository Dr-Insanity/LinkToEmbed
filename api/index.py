from flask import Flask, render_template, send_from_directory, request, send_file
import urllib.parse
import html

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/embed')
def embed():
    base_url = "https://discordembeds.vercel.app/embed?"
    
    slots = [
        "title",
        "description",
        "color",
    ]

    queries_to_metas = {
        "title": '''name="title"''',
        "description": '''name="description"''',
        "color": '''name="theme-color"''',
        "image": '''property="twitter:image"''',
    }

    query = {
        queries_to_metas["title"]: "",
        queries_to_metas["description"]: "",
        queries_to_metas["color"]: "",
        queries_to_metas["image"]: "",
    }

    for embed_feature, embed_value in request.args.items():
        try:
            query[queries_to_metas[embed_feature]] = embed_value
        except KeyError:
            continue

    embed = "<head>\n   "
    for key, value in query.items():
        if key == '''property="twitter:image"''':
            embed += f"""<meta property="twitter:image" content="{html.escape(value)}">"""
        else:
            embed += f"""<meta {key} content="{html.escape(value)}">"""
    embed += "</head>"

    # Build the final URL, including only provided parameters
    embed_url = f"{base_url}{urllib.parse.urlencode(query)}"

    return embed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sitemap.xml')
def sitemap():
    return send_file('../sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_file('../robots.txt')

if __name__ == '__main__':
    app.run()