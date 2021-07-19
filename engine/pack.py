import htmlmin
from os import listdir, mkdir
import os
from os.path import isfile, join, isdir
from engine import logger
def write(name, content):
    temporary = open(name, "w")
    temporary.write(content)
    temporary.close()
def reduce(x, dir):
    if x != "":
        x += "/"
    dirs = [f for f in listdir(x + dir) if isdir(x + dir + "/" + f)]
    files = [f for f in listdir(x + dir) if isfile(x + dir + "/" + f) and f[-5:]==".html"]
    for file in files:
        with open(x + dir + "/" + file) as f: html = f.read()
        html=htmlmin.minify(html, remove_comments=True, remove_empty_space=True).replace('\n',' ').replace('\t',' ').replace('\r',' ')
        write(x + dir + "/" + file, html)       
    
    for directory in dirs:
        reduce(x + dir, directory)
def ignite():
    dirs = [f for f in listdir() if isdir(f)]
    files = [f for f in listdir() if isfile(f) and f[-5:]==".html"]
    for file in files:
        with open(file) as f: html = f.read()
        html=htmlmin.minify(html, remove_comments=True, remove_empty_space=True).replace('\n',' ').replace('\t',' ').replace('\r',' ')
        write(file, html) 
    for d in dirs:
        reduce("", d)   
   
