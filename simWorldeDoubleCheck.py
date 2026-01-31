from random import choice
import matplotlib.pyplot as plt
from datetime import datetime

def setup():
    words=[]
    myFile=open("textFiles/5words.txt","r")
    for eachline in myFile:
        eachline=eachline[:-1].lower().split(" ")
        for eachword in eachline:
            if eachword not in words:
                # could check if word is len = 5
                words.append(eachword)
    return words.copy()

def guess(answer,correct):
    status=[".",".",".",".","."]
    for x in range(len(answer)):
        if answer[x]==correct[x]:
            status[x]=answer[x]
        elif answer[x] in correct:
            status[x]="?"
    return status

def check(status):
    if "." not in status and "?" not in status:
        return True
    return False

def PlayGame(attemps, wordlist):
    wordchoice=choice(wordlist)
    #print(wordchoice)
    for y in range(attemps):
        word=choice(wordlist)
        while len(word)!=5:
            word=input("word: ")
        wordlist.remove(word)
        result = guess(word,wordchoice)
        game=check(result)
        #print(f"Guessed: [{' '.join(word)}]\nGuess {y+1}: [{' '.join(result)}]\n")

        if game:
            return True
        wordlist=AIchoice(wordlist, result, word).copy()
    if not game:
        #print(f"You failed. The word was {wordchoice}")
        return False

def AIchoice(wordslist,result,word):
    temp=[]
    right=[]
    doubleRight=[]
    
    for x in range(len(result)):
        if "." !=result[x]:
            temp.append(word[x])
    targetLetters = set(temp)

    for x in wordslist:
        matches = set(list(x)) & targetLetters
        if len(matches)==len(targetLetters):
            right.append(x)

    for x in right:
        good=False
        bad=False
        for i in range(len(x)):
            if x[i]!=result[i] and result[i]!="." and result[i]!="?":
                bad=True
            elif x[i]==result[i]:
                good=True
                
        if good==True and bad==False:
            # Would performs additional check for "?" placements
            doubleRight.append(x)
            
    if len(doubleRight)==0:
        doubleRight=right.copy()
        
    return doubleRight


wordlists=setup()


start1=datetime.now()
for attempts in range(1,10):
    wins=0
    games=0
    start=datetime.now()
    for y in range(1001):
        result = PlayGame(attempts, wordlists.copy())
        if result:
            wins+=1
        games+=1
        
    end=datetime.now()
    percent=round((wins/games)*100,1)
    print(f"Attempts: {attempts}, Win %: {percent}, Wins: {wins}")
    print(end-start)
    plt.bar(attempts, percent, color = "red")
    
end1=datetime.now()
print(end1-start1)
plt.show()