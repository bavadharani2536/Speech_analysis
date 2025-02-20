import os
from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
from flask_cors import CORS, cross_origin
import shutil, os
import json

from pr_speech_to_text.transcriptGenerator import generateTranscript
from pr_spellingcorrector.spellcorrector import spell_corrector
from pr_keywordspotter.keywordSpotter import AddMultiKeywords


app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True




class ClientService:
    def __init__(self):
        self.FolderPath = "InputFiles"
        self.fileList = os.listdir(self.FolderPath)
        self.separatedOutputFiles = "./Separated_Output_Files"
        self.outputText = {}

    def processAudioFile(self):
        outputResponseObj = {}
        for val in self.fileList:
            inputFileTranscriptedOp = generateTranscript(os.path.join(self.FolderPath,val), self.separatedOutputFiles)
        print(inputFileTranscriptedOp)
        outputResponseObj["inputFileTranscriptedOp"] = inputFileTranscriptedOp

        spellCorrectedOpMap = {}
        for val in inputFileTranscriptedOp.keys():
            spellcorrectedOp = spell_corrector(inputFileTranscriptedOp[val])
            # print("Input Text : ", outputText[val])
            # print("Corrected Text : ", spellcorrectedOp)
            spellCorrectedOpMap[val] = spellcorrectedOp
            # inputFileTranscriptedOp[val] = spellcorrectedOp
        outputResponseObj["spellCorrectedOpMap"] = spellCorrectedOpMap
        print(inputFileTranscriptedOp)

        extractedKeywordMap = {}
        for val in inputFileTranscriptedOp.keys():
            adding = AddMultiKeywords(inputFileTranscriptedOp[val],
                                      {"medium": ["tv ads","newspaper ads","social_media"],
                                       "team": ["manchester united"],
                                       "game": ["football"]})
            result = adding.addkey()
            extractedKeywordMap[val] = result
        outputResponseObj["extractedKeywors"] = extractedKeywordMap

        return outputResponseObj


inputFileDir = "./InputFiles"
archiveDir = './ArchivedInputFiles'


def archiveOldInputFiles():
    files = os.listdir(inputFileDir)
    for f in files:
        if os.path.exists(os.path.join(archiveDir, f)):
            os.remove(os.path.join(archiveDir, f))
        shutil.move(os.path.join(inputFileDir, f), archiveDir)


def processInputFile():
    opResponseObj = clntApp.processAudioFile()
    jsonStr = json.dumps(opResponseObj, ensure_ascii=False).encode('utf8')
    # print(jsonStr.decode())
    return (jsonStr.decode())
    # return Response()


if __name__ == "__main__":
    #this lin will create an object of ClientService Class
    #internally it will call the __init__ function of ClinetService class
    clntApp = ClientService()
    outputVal = processInputFile()
    print(outputVal)
