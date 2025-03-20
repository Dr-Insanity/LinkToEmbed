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

@app.route('/sitemap')
def sitemap():
    return send_file('../sitemap.xml')

@app.route('/robots.txt')
def robots():
    return """robots.txt generated by www.seoptimer.com
User-agent: Googlebot
Disallow: 
User-agent: googlebot-image
Disallow: 
User-agent: googlebot-mobile
Disallow: 
User-agent: MSNBot
Disallow: 
User-agent: Slurp
Disallow: 
User-agent: Teoma
Disallow: 
User-agent: Gigabot
Disallow: 
User-agent: Robozilla
Disallow: 
User-agent: Nutch
Disallow: 
User-agent: ia_archiver
Disallow: /
User-agent: baiduspider
Disallow: 
User-agent: naverbot
Disallow: 
User-agent: yeti
Disallow: 
User-agent: yahoo-mmcrawler
Disallow: 
User-agent: psbot
Disallow: 
User-agent: yahoo-blogs/v3.9
Disallow: 
User-agent: *
Disallow: 
Crawl-delay: 60
Sitemap: https://discordembeds.vercel.app/sitemap
"""

if __name__ == '__main__':
    app.run()