from os import listdir, mkdir
import os
from os.path import isfile, join, isdir
import markdown
from bs4 import BeautifulSoup
from gtts import gTTS
from langdetect import detect
import shutil
from engine import logger
def write(name, content):
    temporary = open(name, "w")
    temporary.write(content)
    temporary.close()
def build(dir):
        configs_file = open(dir + ".config.pagegen")
        configss = configs_file.read()
        settings = configss.split("\n")
        if settings[3] == "slow":
            nspeed = True
        else:
            nspeed = False
        logger.log("deleting previous builds...")
        folders = 0
        bad = 0
        rawdirs = [f for f in listdir(dir) if isdir(join(dir + "/", f)) and f!="markdown"]
        for directory in rawdirs:
            shutil.rmtree(dir + "/" + directory)
            folders += 1
        badfiles = [f for f in listdir(dir) if isfile(join(dir + "/", f)) and f!="index.html" and f!="template.pagegen"]
        for badfile in badfiles:
            os.remove(dir + "/" +  badfile)
            bad += 1
        log = "removed " + str(folders) + "directories and " + str(bad) + "other files"
        logger.log(log)
        
        xml = '<?xml version="1.0" encoding="UTF-8"?><rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:googleplay="http://www.google.com/schemas/play-podcasts/1.0"><channel> <title><![CDATA[' + settings[0] + "]]></title><description><![CDATA[" + settings[1] + ']]></description><link>' + settings[2] + '</link>'
        logger.log("Building blog pages for directory: " + dir)
        home = open(dir + "/index.html")
        home_read = home.read()
        home_point = home_read.split("<!--[[index]]-->")
        home.close()
        template = open(dir + "/template.pagegen")
        template_read = template.read()
        template_point = template_read.split("<!--[content]-->")
        template.close()       
        if len(home_point) != 2:
            logger.log("Did not find properly formatted index page for directory " + dir + ", will proceed with overwriting the page.")
        rawfiles = [f for f in listdir(dir + "/markdown") if isfile(join(dir + "/markdown/", f)) and f[-2:]=="md"]
        allfiles = [f for f in listdir(dir + "/markdown") if isfile(join(dir + "/markdown/", f))]
        diff = list(set(allfiles)-set(rawfiles))
        logger.log("Found these posts: " + str(rawfiles))
        if len(diff) > 0:
            logger.log("Found these files in wrong format (not markdown): " + str(diff))
            logger.log("^ these files will be skipped")
        pi = 1
        failed = 0
        new = ""
        while pi <= len(rawfiles):
                with open(dir + "/markdown/" + str(pi) + ".md") as f: md = f.read()
                logger.log("Rendering " + str(pi) + ".md")
                title = md.split("\n", 2)[0]
                logger.log("Title: " + title)
                html = markdown.markdown(md.split("\n", 2)[2])
                mkdir(dir + "/" + title.lower().replace(" ", "-")[:30])
                clean_text = ' '.join(BeautifulSoup(html, "html.parser").stripped_strings)
                language = detect(clean_text)
                myobj = gTTS(text=clean_text, lang=language, slow=nspeed)
                myobj.save(dir+ "/" + title.lower().replace(" ", "-")[:30] + "/audio.mp3")
                xml += "<item><title>![CDATA[" + title + "]]</title><description><![CDATA[" + html + ']]></description>' + '<link>' + settings[2] + "/" + title.lower().replace(" ", "-")[:30]  + "</link>" + '<guid isPermaLink="true">' + settings[2] + "/" + title.lower().replace(" ", "-")[:30] + "</guid></item>"
                html = '<audio controls><source type="audio/mpeg" src="' + title.lower().replace(" ", "-")[:30] + '/audio.mp3"> Your browser does not support the audio elements.</audio>' + html
                rep = template_point[0] +  html + template_point[1]
                write(dir + "/" + title.lower().replace(" ", "-")[:30] + "/index.html" , rep.replace("[[title]]", title).replace("[[date]]", md.split("\n", 2)[1]))
                if title[:45] == title:
                    n = title
                else:
                    n = title[:45] + "..."
                new = '<br><a href="/' + dir + "/" + title.lower().replace(" ", "-")[:30] + '">' + n + "</a>" + new
                print(new)
                pi = pi + 1
        xml += "</channel></rss>"
        xml = xml.replace("≠", "not-equal-to")
        if new == "":
            new = "<br>there are no posts yet...<br>"
        write(dir + "/feed.xml", xml)
        write(dir + "/index.html", home_point[0] + new + home_point[1])
        if failed != 0:
            logger.log("Number of files failed: " + failed)
            logger.log("^ this was most likely because the files weren't named properly")
        else:
            logger.log("No files were failed")
