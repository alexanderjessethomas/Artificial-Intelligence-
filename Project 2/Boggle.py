# Alex Thomas
# CS470
# Depth First Search
# Assignment 2
# This program runs depth first search on the board provided and gives the total number of moved to complete the board
# It also gives the words found and the total time it took to run the program
# The program outputs the results into a text file
import sys
import math
import time

def createBoard():
    # Get board from text file and put into 2D array
    board = open(sys.argv[1], 'r')
    boardLetters = board.read().replace(' ', '').replace('\n', '')
    boardSize = (int)(math.sqrt(len(boardLetters)))
    boardLayout = [['' for i in range(boardSize)] for i in range(boardSize)]
    for i in range(len(boardLetters)):
        boardLayout[i%boardSize][i//boardSize] = boardLetters[i]
    return boardLayout

def createDictionary():
    comparisonDictionary = open(sys.argv[2], 'r')
    comparisonTree = dict()
    for dictionaryWord in (textLine.strip() for textLine in comparisonDictionary):
        currentIndex = comparisonTree
        for letter in dictionaryWord:
            if letter in currentIndex:
                currentIndex = currentIndex[letter]
            else:
                currentIndex[letter] = {}
                currentIndex = currentIndex[letter]
        currentIndex["stop"] = "stop"
    return comparisonTree

def searchDictionary(word, comparisonDictionary):
    comparisonDictionary = comparisonDictionary
    words = ''
    for index in word:
        words += index.lower()
        if index in comparisonDictionary:
            comparisonDictionary = comparisonDictionary[index]
            if words == word  and "stop" in index:
                return 'completeword'
            elif words == word:
                return 'almostcompleteword'
    return False

def dfsearch(coordX, coordY, word, searched, boardLayout, comparisonDictionary, located):
    word += boardLayout[coordX][coordY]
    located[0].append('a')
    if searchDictionary(word.lower(), comparisonDictionary) == 'completeword':
        located[len(word)].append(word)
    if searchDictionary(word.lower(), comparisonDictionary) in ['almostcompleteword', 'completeword']:
        searched.append(str(coordX) + ',' + str(coordY))
        for i in range(len(boardLayout)):
            for k in range(len(boardLayout)):
                if i >= 0 and i < len(boardLayout) and i >= (coordX - 1) and i <= (coordX + 1):
                    if k >= 0 and k < len(boardLayout) and k >= (coordY - 1) and k <= (coordY + 1):
                        if ((i == coordX and k == coordY) == False) and (str(i) + ',' + str(k)) not in searched:
                            dfsearch(i, k, word, list(searched), boardLayout, comparisonDictionary, located)

def helper (boardLayout, comparisonDictionary):
    located = [[] for i in range(((len(boardLayout))*(len(boardLayout)))+1)]
    for i in range(len(boardLayout)):
        for j in range(len(boardLayout)):
            dfsearch(i, j, '', [], boardLayout, comparisonDictionary, located)
    return located

dictionary = createDictionary()
board = createBoard()
output = open('results.txt', 'w')
startSearchTime = time.time()
located = helper(board, dictionary)
endSearchTime = time.time() - startSearchTime
output.write('Alex Thomas CS470\n2/27/2017\nDr. Doerry')
output.write('Depth First Search on following board: \n')
output.write(open(sys.argv[1], 'r').read())
locatedWords = []
for i in range(2, len(located)):
    if len(located[i]) > 0:
        output.write(str(i) + " letter words: ")
        for word in list(set(located[i])):
            output.write(word + ", ")
        output.write('\n')
        locatedWords += located[i]
        locatedWords.sort()
locatedWords.sort()
output.write("All words: " + str(list(set(locatedWords))) + '\n')
output.write('Located ' + str(len(list(set(locatedWords)))) + "words\n")
output.write("Time ran: " + str(endSearchTime) + "seconds \n")
output.write("Total number of moves to complete: " + str(len(located[0])))
