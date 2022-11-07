#!/bin/python3
import deepl
import json
import os

folderPathsToTranslate = [
    ("./overlay/ja", "./overlay/en-deepl"),
    ("./bin/ja", "./bin/en-deepl")
]

pathsToCreate = [
    "./overlay/en-deepl/",
    "./bin/en-deepl/",
    "./bin/en-deepl/data",
    "./bin/en-deepl/sec",
    "./bin/en-deepl/ses",
    "./bin/en-deepl/soc",
]

for path in pathsToCreate:
    try:
        os.makedirs(path, exist_ok=True)
    except:
        pass

with open("./secrets.json") as secretsFile:
    secrets = json.loads(secretsFile.read())

def translateText(text):
    if(text.isascii()):
        return text
    else:
        translated_text = []
        translator = deepl.Translator(secrets["DeepLKey"])

        for line in text.split('\n'):
            try:
                result = translator.translate_text(line, target_lang="EN-GB") 
                translated_text.append(result.text)
                print(text, "->", '\n'.join(translated_text))
            except:
                translated_text.append("")
        return '\n'.join(translated_text)

for folderPathToTranslate in folderPathsToTranslate:
    for folderTree in os.walk(folderPathToTranslate[0]):
        for file in folderTree[2]:
            jsonPath = folderTree[0] + "/" + file
            print("\n" + jsonPath)

            with open(jsonPath, 'r', encoding="utf-8") as jsonFile:
                translationData = json.loads(jsonFile.read())
                newTranslationData = []

                if (type(translationData) == list):
                    for text in translationData:
                        newTranslationData.append(translateText(text))

                    translationData = newTranslationData
                else:
                    for translationKey in translationData.keys():
                        translationData[translationKey] = translateText(translationData[translationKey])

                with open(jsonPath.replace(folderPathToTranslate[0], folderPathToTranslate[1]), 'w', encoding="utf-8") as jsonFile:
                    jsonFile.write( json.dumps(translationData, indent=4, ensure_ascii=False) )