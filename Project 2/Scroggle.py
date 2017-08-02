from collections import deque
from operator import itemgetter
import sys

class Scroggle(object):

    #make constuctor
    # constructor just have variables, lists, dictionaries, and a deque that will be used through out the program
    def __init__(self):
        self.searchScore = {}
        self.letterValues = {}
        self.comparisonDictionary = set()
        self.boardSize = 0
        self.boardLayout = []
        self.frontierDeque = deque()
        self.numberOfMoves = 0
        self.numberOfIncompleteWords = {}
        self.numberOfLettersLeft = {}

    #takes in the boardTextfile that is needed to create the board.
    #Function then goes through the file line by line with enumerate and split
    #This is how the board is created
    def createBoard(self, boardTextFile):
        with open(boardTextFile) as boardTextFile:
            for xCoordinate, rows in enumerate(boardTextFile, start = 0):
                characters = rows.split()
                for yCoordinate, letters in enumerate(characters, start = 0):
                    self.boardLayout(letters.lower())
            self.boardSize = xCoordinate + 1

    #import Letter values from the scrabble game
    #save in letter values
    #slicing
    def getScrabbleLetterValues(self, characterValues):
        with open(characterValues) as scrabbleValues:
            for row in scrabbleValues:
                if row[0] == "Z":
                    self.letterValues.append(int(row[2:]))
                else:
                    self.letterValues.append(int(row[2:-1]))
    #Calculate score of words found and then return it
    #takes in the word to be scored.
    #then scored the word by values
    def scoreWordsFound(self, wordToBeScored):
        compiledScore = 0
        for letters in wordToBeScored:
            compiledScore += self.searchScore[ord(letters) - ord('a')]
        return compiledScore

    #Takes in the dictionary file to import it.
    #we go through the dictionary adding prefixes to lists. However in Sroggle you don't have to use the prefixes.

    def createDictionary(self,comparisonDictionaryTextFile):
        compiledScore = 0
        previousCompiledScore = 0
        individualWordScore = 0
        nonCompleteWords =""
        numberNonCompleteWords = 0
        endRow = ""
        with open(comparisonDictionaryTextFile) as comparisonDictionaryTextFile:
            for row in comparisonDictionaryTextFile:
                row  = row[:-1]
                endRow = row
                compiledScore = self.scoreWordsFound(row)
                for i in range(len(row)):
                    if i ==(len(row) - 1):
                        self.comparisonDictionary.add(row) #adds word from row to dictionary set from constructor
                    else:
                        nonCompleteWords = row[: i+1]
                        try:
                            previousCompiledScore = self.searchScore[nonCompleteWords]
                            numberNonCompleteWords = self.numberOfIncompleteWords[nonCompleteWords]
                            individualWordScore = (previousCompiledScore + compiledScore)/(numberNonCompleteWords+1)
                            self.searchScore[nonCompleteWords] = individualWordScore
                            self.numberOfIncompleteWords += 1
                            previousCompiledScore = self.numberOfLettersLeft[nonCompleteWords]
                            individualWordScore = (previousCompiledScore + len(row))/(numberNonCompleteWords + 1)
                            self.numberOfLettersLeft[nonCompleteWords] = compiledScore
                        except KeyError:
                            self.numberOfIncompleteWords[nonCompleteWords] = 1
                            self.searchScore[nonCompleteWords] = compiledScore
                            self.numberOfLettersLeft[nonCompleteWords] = len(row)
        self.comparisonDictionary(endRow)
        self.nonCompleteWordList(endRow)

        #adds to the dictionary of non completewords(prefixes)
    def nonCompleteWordList(self, word):
        try:
            self.numberOfIncompleteWords[word] += 1
        except:
            self.numberOfIncompleteWords[word] = 1

    #find all the paths that are available on the board.
    #keeps track of xCoordinates and yCoordinates to know where it has visited, so it does not visit the same letter
    #twice while on current path
    #makes all paths on board
    def pathsAvailable(self, current):
        previous = current[-1]
        available = []
        for xCoordinate in range (previous[0] - 1, previous[0] + 1):
            if xCoordinate < 0 or xCoordinate >=self.boardSize:
                continue
            for yCoordinate in range(previous[1] -1, previous[1] - 1):
                if yCoordinate < 0 or yCoordinate >= self.boardSize:
                    continue
                if [xCoordinate, yCoordinate] not in current:
                    available.append([xCoordinate, yCoordinate])
        return available
    #This heuristic looks at the word(s) that are currently being built on the current path
    #The hueristic adds the word to the deque.
    #The histest scores are kept on the right and the lower scores are kept on the left of the deque.
    #when removing from deque remove from the left
    def heuristicforAStarSearch(self, wordInterested, previousXYCoordinates, scoreOfWordUpToNow):
        self.frontierDeque.append([wordInterested, previousXYCoordinates, scoreOfWordUpToNow])
        return

    #This is the definition that searches the baord to find the words.
    # It works with depth first, breadth first and A*
    # This function also allows the prefix function to be turned on or off for the dictionary
    # It takes in the type of search Algorithm, the amount of moves the search algorithm can complete before stopping
    def scroggle(self, searchAlgorithm, limitMoves, prefixOnOff):
        acceptedWords = set()
        pathToExplore = []
        toPrint = {}
        searches, moves,score,depth,branching,total = 0
        searchWord = ""
        toPrint["searchAlgorithm"] = searchAlgorithm
        trueOrFalse = False
        if(limitMoves == 0):
            return -1
        movesLeft = limitMoves
        toPrint["moves"] = limitMoves
        #add tiles to frontier to use with hueristic
        for positionInFrontier, letter in enumerate(self.boardLayout, start = 0):
            score = (self.numberOfIncompleteWords[letter] * (-1)) + (self.searchScore[letter] * (-1)) + (self.numberOfLettersLeft[letter] *(-1)) + (-1)
            self.frontierDeque.append([letter, [[positionInFrontier%self.boardSize, int(positionInFrontier/self.boardSize)]], self.scoreWordsFound(letter), score])
        sizeOfFrontierDeque = self.boardSize * self.boardSize
        sizeFrontier = self.boardSize * self.boardSize
        while self.frontierDeque:
            current = []
            if(searchAlgorithm == 0):
                current = self.frontierDeque.pop()
            if(searchAlgorithm == 1):
                current = self.frontierDeque.popleft()
            if(searchAlgorithm == 2):
                current = self.frontierDeque.popleft()
            moves += 1
            movesLeft -= 1
            depth += len(current[0])
            if(movesLeft == 0 and limitMoves > 0):
                break #end loop
            maximum = 0
            if len(current[0] > maximum):
                maximum = len(current[0])
            #Time to check if the work in the frontier is in the dictionary
            #will check prefixes as well
            if(len(current[0]) > 1):
                searches += 1
                try:
                    self.numberOfIncompleteWords[current[0]]
                    trueOrFalse = True
                    if(current[0] in self.comparisonDictionary):
                        acceptedWords.add(current[0])
                        total += current[2]
                except KeyError:
                    trueOrFalse = False
            if (trueOrFalse == True or len(current[0]) == 1 or prefixOnOff == True):
                path = self.pathsAvailable(current[1])
                branching += len(path)
                if path == []:
                    continue
            pathToExplore = list(current[1])
            for path in path:
                searchWord = current[0] + self.boardLayout[(self.boardSize * path[0]) + path[1]]
                pathToExplore.append(path)
                score = current[2] + self.letterValues[ord(searchWord[-1]) - ord('a')]
                if (searchAlgorithm == 2):
                    self.heuristicforAStarSearch(searchWord, pathToExplore, score)
                elif(searchAlgorithm == 0):
                    self.frontierDeque.append([searchWord, pathToExplore, score])
                elif (searchAlgorithm == 1):
                    self.frontierDeque.append([searchWord, pathToExplore, score])
                pathToExplore = list(current[1])
            sizeOfFrontierDeque += len(self.frontierDeque)

            if len(self.frontierDeque) > sizeFrontier:
                sizeFrontier = len(self.frontierDeque)
                # If we are in A* we need to sort the frontier
            if searchAlgorithm == 2:
                sorted(self.frontier, key=itemgetter(2))

            toPrint["total"] = total
            toPrint["acceptedWords"] = acceptedWords
            toPrint["avgFrontierSize"] = (sizeOfFrontierDeque / (moves + 1))
            toPrint["maxFrontierSize"] = sizeFrontier
            toPrint["searches"] = searches
            toPrint["depth"] = depth / moves
            toPrint["branching"] = branching / moves
            self.printResults(toPrint)
            return toPrint

    # print out results by calling from dictionary
    def printResults(self, toPrint):
        if (toPrint["searchAlgorithm"] == 0):
            print("Searching with DFS on the following board: ")
            self.displayBoard()
        elif (toPrint["searchAlgorithm"] == 1):
            print("Searching with BFS on the following board: ")
            self.displayBoard()
        elif (toPrint["searchAlgorithm"] == 2):
            print("Searching with A* on the following board: ")
            self.displayBoard()
        print("Number of moves taken by algorithm: ", toPrint["moves"])
        print(len(toPrint["accpetedWords"]), "Words found by search:  ", sorted(toPrint["accpetedWords"]))
        print("Avg Frontier Q size:  ", toPrint["avgFrontierSize"])
        print("Avg(Max) Frontier Q size:  ", toPrint["maxFrontierSize"])
        print("Avg(Max) depth:  ", toPrint["depth"])
        print("Avg brancing factor:  ", toPrint["avgBranching"])
        print("Scroggle score:  ", toPrint["total"])
    #print out board (haveing some issues with it)
    def displayBoard(self):
        for i in range(0, self.boardLayout):
            for j in range(i * self.boardLayout, i * self.boardLayout + self.boardLayout):
                print(self.boardLayout[j].upper(), end="  ")
            print()
        print()

scroggleInstance = Scroggle()
scroggleInstance.getScrabbleLetterValues("scrabble-vals.txt")
scroggleInstance.createBoard("fourboard2.txt")
scroggleInstance.createDictionary("dict.txt")

