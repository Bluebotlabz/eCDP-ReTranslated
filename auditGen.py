#!/bin/python3
import csv
import json
import os

folderPathsToTranslate = [
    ("./overlay/ja", "./overlay/en-deepl", "./overlay/en-og", "./overlay/data"),
    ("./bin/ja", "./bin/en-deepl", "./bin/en-og")
]

with open("./auditTranslations.csv", mode='w', newline='', encoding='utf-8') as file:
        file.write( ','.join( ("japaneseText", "originalTranslation", "translatedText", "maxLength") ) + "\n" )

def escapeCSVText(text):
    return '"' + str(text).replace('\n', '\\n').replace('"', '""') + '"'

def saveData(japaneseText, translatedText, originalTranslation, maxLength=False):
    #if (not maxLength):
    #    maxLength = len(japaneseText)

    maxLength = len(originalTranslation)

    #if (len(translatedText) > maxLength or "(" in translatedText):
    with open("./auditTranslations.csv", mode='a', newline='', encoding='utf-8') as file:
        file.write( ','.join( (escapeCSVText(japaneseText), escapeCSVText(originalTranslation), escapeCSVText(translatedText), escapeCSVText(maxLength)) ) + "\n" )

    print(japaneseText, "->", translatedText)
    return translatedText

for folderPathToTranslate in folderPathsToTranslate:
    for folderTree in os.walk(folderPathToTranslate[0]):
        for file in folderTree[2]:
            jsonPath = folderTree[0] + "/" + file
            print("\n" + jsonPath)

            with open(jsonPath, 'r', encoding="utf-8") as jsonFile:
                translationData = json.loads(jsonFile.read())
                
                with open(jsonPath.replace(folderPathToTranslate[0], folderPathToTranslate[1]), 'r', encoding="utf-8") as file:
                    translatedData = json.loads(file.read())

                with open(jsonPath.replace(folderPathToTranslate[0], folderPathToTranslate[2]), 'r', encoding="utf-8") as file:
                    originalTranslatedData = json.loads(file.read())
                
                newTranslationData = []

                if (type(translationData) == list):
                    for i in range(len(translationData)):
                        saveData(translationData[i], translatedData[i], originalTranslatedData[i])

                    translationData = newTranslationData
                else:
                    with open(jsonPath.replace(folderPathToTranslate[0], folderPathToTranslate[3]), 'r', encoding="utf-8") as file:
                        memoryData = json.loads(file.read())

                    for translationKey in translationData.keys():
                        memoryLength = False
                        # Find memory length:
                        for stringData in memoryData["strings"]:
                            if (str(stringData["rom_address"]) == translationKey):
                                memoryLength = int(stringData["blen"])
                                break

                        saveData(translationData[translationKey], translatedData[translationKey], originalTranslatedData[translationKey], memoryLength)