from os import listdir, mkdir
import os
import markdown
import shutil
from engine import logger
import yaml
import requests

def write(name, content):
    temporary = open(name, "w")
    temporary.write(content)
    temporary.close()
def build(dir):   
        home = open(dir + "/template.pagegen")
        home_read = home.read()
        home_point = home_read.split("<!--[content]-->")
        home.close()
        stream = open(dir + "/links.yaml", 'r')
        linkp = yaml.load(stream)
        tscript = False
        html = home_point[0]
        links = linkp["links"]
        if len(home_point) != 2:
            logger.log("Did not find properly formatted index page for directory " + dir + ", will proceed with overwriting the page.")
            home_point.append("")
        for l in links.items():
            try:
                ltype = l[1]["t"]
                title = l[0]
                try:
                    url = l[1]["v"]
                except:
                    print()
                if ltype == "tweet":
                    r = requests.get(url = "https://publish.twitter.com/oembed?url=" + url + "&maxwidth=10px&limit=1&dnt=1")
                    data = r.json()
                    if tscript:
                        html += '<center><br>' + "\n".join(data["html"].split("\n")[:-2]) + "</center>"
                    else:
                        html += '<center><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script><br>' + "\n".join(data["html"].split("\n")[:-2]) + "</center>"
                        tscript = True
                elif ltype == "spotify":
                    html += '<br><center><br><iframe  src="' + url.replace("spotify.com", "spotify.com/embed") + '" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe></center>'
                elif ltype == "link":
                    html += """<br><button onclick="window.location.href='""" + url + """'">""" + title + "</button>"
                elif ltype == "text":
                    html += '<p style="text-align: center">' + title + "</p>"
                else:
                    logger.log("Couldn't find appropriate code for item type " + ltype)
            except:
                logger.log("No type provided, skipping.")
        html += home_point[1]
        write(dir + "/index.html", html)
            
                