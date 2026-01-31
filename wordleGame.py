import random
from itertools import permutations
from string import ascii_lowercase
import enchant
import time
import re
import multiprocessing as mp

def useCore(func, array, *arg, cores=mp.cpu_count()):
    processes = []
    manager = mp.Manager()
    return_list = manager.list()
    segmentSize = len(array)/cores
    #print("Segment size of:", segmentSize) # optional

    startTime = time.time() # optional
    for i in range(0, cores):
        newArr = array[int(i*segmentSize):int((i+1)*segmentSize)]
        p = mp.Process(target=func, args=(newArr, return_list, arg,))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()

    endTime = time.time() # optional
    timeElapse = endTime-startTime # optional
    print(f'That took {timeElapse} seconds') # optional
    return return_list

def isValidWord(arr, returnList, _):
    GBD = enchant.Dict("en_GB")
    for x in arr:
        # value = "".join(x)
        if GBD.check(x):
            returnList.append(x)

def getWord():
    value="zz"
    while not GBD.check(value):
        value = input("Enter a word: ")
    return value

def containsChr(arr, returnList, *arg):
    containArg = arg[0][0]
    for word in arr:
        invalid = False
        for let in containArg:
            if let not in word:
                invalid = True
                break
        if not invalid:
            returnList.append(word)

def notContainsChr(arr, returnList, *arg):
    notContainArg = arg[0][0]
    for word in arr:
        invalid = False
        for let in notContainArg:
            if let in word:
                invalid = True
                break
        if not invalid:
            returnList.append(word)

def correctChr(arr, returnList, *arg):
    correctArg = arg[0][0]
    temp = []
    for let in correctArg:
        if let == "":
            temp.append(".")
        else:
            temp.append(let)
    check = f"{''.join(temp)}"
    for word in arr:
        result = re.match(check, word) # compares input to regex expression
        if result: # if result is true, ends while loop
            returnList.append(word)


if __name__ == '__main__':
    length = 5

    #allValidWords = ["spawn","slick","prick","cramp","sight","brick","slime","space","words","check","crpyt"]

    GBD = enchant.Dict("en_GB")
    #possible = list(permutations(ascii_lowercase, length))
    possible = list(map("".join, permutations(ascii_lowercase, length)))
    print("started filterisation")
    allValidWords = list(useCore(isValidWord, possible))
    print("Finished filterisation... Choosing word to guess")

    toGuess = random.choice(allValidWords)
    #toGuess = "brick"
    guessed = False

    contains = []
    notContains = []
    correct = ["","","","",""]
    while not guessed:
        guess = getWord()
        if toGuess == guess:
            print("word guessed")
            break

        for let in guess:
            if let in list(toGuess):
                if let not in contains:
                    contains.append(let)
            else:
                if let not in notContains:
                    notContains.append(let)
        for x in range(length):
            if toGuess[x] == guess[x]:
                correct[x] = guess[x]
        print(contains)
        print(correct)

        arr = []
        #newValid1 = containsChr(allValidWords, arr, contains)
        newValid1 = list(useCore(containsChr, allValidWords, contains))
        newValid2 = list(useCore(notContainsChr, newValid1, notContains))
        newValid3 = list(useCore(correctChr, newValid2, correct))
        #asd = correctChr(newValid2, arr, correct)
        if len(newValid3)<15:
            print(newValid3)
