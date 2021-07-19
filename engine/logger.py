def write(name, content):
    temporary = open(name, "a")
    temporary.write(content)
    temporary.close()

def log(log):
    print(log)
    log = log + "\n"
    write("logs.txt", log)

