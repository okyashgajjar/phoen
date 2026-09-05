import glob
for f in glob.glob("src/components/*.jsx"):
    with open(f, "r") as file:
        content = file.read()
    content = content.replace("\\'", "'")
    with open(f, "w") as file:
        file.write(content)
