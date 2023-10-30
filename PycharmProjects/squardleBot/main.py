import time
import pyautogui
import pytesseract
import cv2
import os
import numpy as np

os.environ['TESSDATA_PREFIX'] = '/Users/joseph_kelly/homebrew/Cellar/tesseract/5.3.3/share/tessdata'
pytesseract.pytesseract.tesseract_cmd = '/Users/joseph_kelly/homebrew/bin/tesseract'

# TEXT TO ARRAY

# Screen Shot from (820, 380) to (1120, 680)

im_gray = cv2.imread('squardle10:18.TIFF', cv2.IMREAD_GRAYSCALE)
cv2.rectangle(im_gray, (0, 115), (600, 165), 255, -1)
cv2.rectangle(im_gray, (0, 275), (600, 325), 255, -1)
cv2.rectangle(im_gray, (0, 435), (600, 485), 255, -1)
cv2.rectangle(im_gray, (125, 0), (165, 600), 255, -1)
cv2.rectangle(im_gray, (275, 0), (325, 600), 255, -1)
cv2.rectangle(im_gray, (435, 0), (485, 600), 255, -1)

(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

text = pytesseract.image_to_string(im_gray, config='--psm 6')
text = text.replace("OD", 'D')
text = text.replace("S$", 'S')
text = text.replace(" ", '')
text = text.replace("\n", '')

letterArray = np.array([
    [text[0], text[1], text[2], text[3]],
    [text[4], text[5], text[6], text[7]],
    [text[8], text[9], text[10], text[11]],
    [text[12], text[13], text[14], text[15]]
])

print(letterArray)

# SQUARDLE SOLVER

with open("recognized.txt", "w") as file:
    pass

with open("SquardleWL.txt", "r") as file:
    words = file.readlines()

for i in range(len(words)):
    words[i] = words[i].replace("\n", "")

visitedArray = np.zeros((4, 4), dtype=bool)  # Initialize a 4x4 visitedArray

ROW = 3
COL = 3
dRow = [-1, 1, 0, 0, -1, -1, 1, 1]
dCol = [0, 0, -1, 1, -1, 1, -1, 1]

def isValid(row, col):
    if row < 0 or col < 0 or row >= ROW or col >= COL:
        return False

    if visitedArray[row][col]:
        return False

    return True

def isWordInList(word, word_list):
    return word in word_list

def generateWordsDFS(row, col, grid, path, word_list, max_depth):
    print(path)
    if len(path) >= 4 and isWordInList(path, word_list):
        with open("recognized.txt", "a") as file:
            print(path)
            file.write(path + '\n')

    if len(path) > max_depth:
        return  # Limit the depth of recursion



    for i in range(8):
        newRow = row + dRow[i]
        newCol = col + dCol[i]

        if isValid(newRow, newCol):
            visitedArray[newRow][newCol] = True
            newPath = path + grid[newRow][newCol]
            generateWordsDFS(newRow, newCol, grid, newPath, word_list, max_depth)
            visitedArray[newRow][newCol] = False

def findWordsInGrid(grid, word_list):
    for i in range(ROW):
        for j in range(COL):
            visitedArray = np.zeros((ROW, COL), dtype=bool)  # Reset the visitedArray for each starting cell
            visitedArray[i][j] = True
            path = grid[i][j]
            generateWordsDFS(i, j, grid, path, word_list, max_depth=15)

findWordsInGrid(letterArray, words)

with open("recognized.txt", "r") as file:
    recognized = file.readlines()


time.sleep(2)
for i in range(len(recognized)):
    if recognized[i] != "\n":
        pyautogui.typewrite(recognized[i], 0.1)
    else:
        pyautogui.typewrite('\n', .5)

# cv2.imshow('Result', im_bw)
# cv2.waitKey(0)