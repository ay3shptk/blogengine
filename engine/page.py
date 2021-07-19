from os import listdir, mkdir
import os
from os.path import isfile, join, isdir
import markdown
import shutil
from engine import logger
def write(name, content):
    temporary = open(name, "w")
    temporary.write(content)
    temporary.close()
def build(dir):
        if dir != "":
            dir = dir + "/"      
        template = open(dir + "template.pagegen")
        template_read = template.read()
        template_point = template_read.split("<!--[content]-->")
        template.close()
        if len(template_point) != 2:
            logger.log("Did not find properly formatted index page for directory " + dir + ", will proceed with overwriting the page.")
        rawfiles = [f for f in listdir(dir) if isfile(join(dir, f)) and f[-2:]=="md"]
        allfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
        diff = list(set(allfiles)-set(rawfiles))
        logger.log("Found these posts: " + str(rawfiles))
        if len(diff) > 0:
            logger.log("Found these files that were not markdown: " + str(diff))
            logger.log("^ these files will be skipped")
        failed = 0
        new = ""
        for file in rawfiles:
            with open(dir + "/" + file) as f: md = f.read()
            logger.log("Rendering " + file)
            title = md.split("\n", 1)[0]
            logger.log("Title: " +  title)
            html = markdown.markdown(md.split("\n", 1)[1])
            try:
                mkdir(dir + file[:-3])
            except:
                shutil.rmtree(file[:-3])
                mkdir(dir + file[:-3])
            hehe =  template_point[0] + html + template_point[1]
            write(dir + file[:-3] + "/index.html", hehe.replace("[[title]]", title))               

