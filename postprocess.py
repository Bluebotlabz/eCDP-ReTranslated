#!/bin/python3
import math
import json
import os

langName = 'en'

folderPathsToTranslate = [
    ("./overlay/ja", "./overlay/" + langName, "./overlay/en-deepl", "./overlay/en-og", "./overlay/data"),
    ("./bin/ja", "./bin/" + langName, "./bin/en-deepl", "./bin/en-og")
]

pathsToCreate = [
    "./overlay/" + langName,
    "./bin/" + langName,
    "./bin/" + langName + "/data",
    "./bin/" + langName + "/sec",
    "./bin/" + langName + "/ses",
    "./bin/" + langName + "/soc",
]

for path in pathsToCreate:
    try:
        os.makedirs(path, exist_ok=True)
    except:
        pass

global translationsMissing
translationsMissing = 0

whitelistedUnicode = [
    '①',
    '②',
    '③',
    '④',
    '⑤',
    '⑥',
    '⑦',
    '⑧',
    '⑨',
    '⑩',
    '⑪',
    '⑫',
    '０',
    '１',
    '２',
    '３',
    '４',
    '５',
    '６',
    '７',
    '８',
    '９',
    'Ａ',
    'Ｂ',
    'Ｃ',
    'Ｄ',
    'Ｅ',
    'Ｆ',
    'Ｇ',
    'Ｈ',
    'Ｉ',
    'Ｊ',
    'Ｋ',
    'Ｌ',
    'Ｍ',
    'Ｎ',
    'Ｏ',
    'Ｐ',
    'Ｑ',
    'Ｒ',
    'Ｓ',
    'Ｔ',
    'Ｕ',
    'Ｖ',
    'Ｗ',
    'Ｘ',
    'Ｙ',
    'Ｚ',
    'ｅ',
    '℃',
    '°C'
]

deUnifiedText = str.maketrans({
    'Ａ': 'A',
    'Ｂ': 'B',
    'Ｃ': 'C',
    'Ｄ': 'D',
    'Ｅ': 'E',
    'Ｆ': 'F',
    'Ｇ': 'G',
    'Ｈ': 'H',
    'Ｉ': 'I',
    'Ｊ': 'J',
    'Ｋ': 'K',
    'Ｌ': 'L',
    'Ｍ': 'M',
    'Ｎ': 'N',
    'Ｏ': 'O',
    'Ｐ': 'P',
    'Ｑ': 'Q',
    'Ｒ': 'R',
    'Ｓ': 'S',
    'Ｔ': 'T',
    'Ｕ': 'U',
    'Ｖ': 'V',
    'Ｗ': 'W',
    'Ｘ': 'X',
    'Ｙ': 'Y',
    'Ｚ': 'Z',
    '０': '0',
    '１': '1',
    '２': '2',
    '３': '3',
    '４': '4',
    '５': '5',
    '６': '6',
    '７': '7',
    '８': '8',
    '９': '9'
})

shortenedText = {
    ' Hours': 'hrs',
    ' Minutes': 'mins',
    ' Seconds': 'sec',
    ' hours': 'hrs',
    ' minutes': 'mins',
    ' seconds': 'sec',
    ' hour': 'hr',
    ' Hour': 'hr'
}

def whitelistText(text):
    for char in whitelistedUnicode:
        text = text.replace(char, '')

    return text

def toBullet(text, pointChar='■', pointLength=16):
    if (len(text) < pointLength):
        return text
    
    #text = text.replace('\n','')
    newText = []

    if (not pointChar in text.split("\n")[0]):
        offset = len(text.split("\n")[0]) # Set the offset to ignore the title
        newText.append(text.split("\n")[0])
    else:
        offset = 0

    splitAmount = math.floor((len(text) - offset)/pointLength)
    for i in range(splitAmount+1):
        if (i == splitAmount+1):
            newText.append(text[(pointLength*i) + offset:])
        else:
            newText.append(text[(pointLength*i) + offset:(pointLength*(i+1)) + offset])

    return '\n'.join(newText)

def translateText(japaneseText, translatedText, originalTranslation, filename, isOverlay=False):
    global translationsMissing

    if (not whitelistText(originalTranslation).isascii()): # No translation available
        print("\n")
        print("No Translation Found For [" + str(originalTranslation).replace('\n', '\\n') + "]")
        print("Using DeepL Translation: [" + str(translatedText).replace('\n', '\\n') + "]")

        translationsMissing += 1

        print(japaneseText.replace('\n', '\\n'), "->", translatedText.replace('\n', '\\n'))

        if ('sec' in filename): # Translate self-check quiz
            translatedText = toBullet(translatedText.replace('\n', ''), pointChar='', pointLength=25)

            for textToShorten in shortenedText.keys():
                translatedText.replace(textToShorten, shortenedText[textToShorten])

        elif ("■" in translatedText):
            return toBullet(translatedText)

        if (not isOverlay): # Length restriction is not present in non-overlay texts
            return translatedText.translate(deUnifiedText)
        else:
            # Shorten overlay text
            for textToShorten in shortenedText.keys():
                translatedText.replace(textToShorten, shortenedText[textToShorten])
            if (translatedText[-1] == '.' and translatedText[-2] != '.'):
                translatedText = translatedText[:-1]

            # Overlay translations need to be shortened due to limited space
            if (len(originalTranslation)+11 >= len(translatedText)):
                return translatedText.translate(deUnifiedText) # Length limit for overlay
            elif (len(originalTranslation)+3 >= len(translatedText)):
                return translatedText.translate(deUnifiedText) # If the ... is not needed, just return the whole text
            else:
                return (translatedText[:round(len(originalTranslation))] + '...').translate(deUnifiedText) # Remove unicode from text

    else: # If there is already a translation available
        return originalTranslation.translate(deUnifiedText) # Still remove unicode anyway

for folderPathToTranslate in folderPathsToTranslate:
    for folderTree in os.walk(folderPathToTranslate[0]):
        for file in folderTree[2]:
            jsonPath = folderTree[0] + "/" + file
            print("\n" + jsonPath)

            with open(jsonPath, 'r', encoding="utf-8") as jsonFile:
                translationData = json.loads(jsonFile.read())
                
                with open(jsonPath.replace(folderPathToTranslate[0], folderPathToTranslate[2]), 'r', encoding="utf-8") as file:
                    translatedData = json.loads(file.read())

                with open(jsonPath.replace(folderPathToTranslate[0], folderPathToTranslate[3]), 'r', encoding="utf-8") as file:
                    originalTranslatedData = json.loads(file.read())
                
                newTranslationData = []

                if (type(translationData) == list):
                    for i in range(len(translationData)):
                        newTranslationData.append(translateText(translationData[i], translatedData[i], originalTranslatedData[i], jsonPath, isOverlay=False))

                    translationData = newTranslationData
                else:
                    with open(jsonPath.replace(folderPathToTranslate[0], folderPathToTranslate[4]), 'r', encoding="utf-8") as file:
                        memoryData = json.loads(file.read())
                    
                    for translationKey in translationData.keys():
                        translationData[translationKey] = translateText(translationData[translationKey], translatedData[translationKey], originalTranslatedData[translationKey], jsonPath, isOverlay=True)

                with open(jsonPath.replace(folderPathToTranslate[0], folderPathToTranslate[1]), 'w', encoding="utf-8") as jsonFile:
                    jsonFile.write( json.dumps(translationData, indent=4, ensure_ascii=False) )

print("\n\n")
print("Added", str(translationsMissing), "missing translations")