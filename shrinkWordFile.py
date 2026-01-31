# This script reads a file named "words.txt" containing a list of words
# and writes all five-letter words to a new file named "5words.txt".
allWordsFile=open("textFiles/words.txt","r")
fiveLetterWordsfile=open("textFiles/5words.txt","w")
words=[]
for eachline in allWordsFile:
    if len(eachline[:-1])==5:
        fiveLetterWordsfile.write(eachline)
allWordsFile.close()
fiveLetterWordsfile.close() 
