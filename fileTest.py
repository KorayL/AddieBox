import os

fileList = os.listdir("../Addie-Box-Data")
fileList.remove(".git")
fileList.remove(".gitattributes")
print(fileList)

