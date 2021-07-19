import json
import requests
from engine import logger
def ignite():
    def write(name, content):
        temporary = open(name, "w")
        temporary.write(content)
        temporary.close()
    external = open("tasks.json")
    tasks = json.load(external)
    external.close()
    logger.log("Found these tasks to mirror files: \n\n" + str(tasks["create"]))
    for task in tasks["create"]:
        url = task["link"]
        logger.log("Requesting " + url)
        r = requests.get(url = url)
        logger.log("Mirroring to " + task["filename"])
        write(task["filename"], r.text)
        logger.log(task["filename"] + " was mirrored from " + url)
    logger.log("Tasks list completed.")