#importing required module
import PyPDF2
from gtts import gTTS
import os
#create a file obj and open in read binary mode
pdfFileObj = open('sample.pdf','rb')     #'rb' for read binary mode
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0)          #'9' is the page number
p=pageObj.extractText()
#close
pdfFileObj.close()
#set language
lang='en'
#passing the text and slow=false bcz i want the audio have a high  speed
myobj=gTTS(text=p,lang=lang,slow=False)
#save it in mp3 file
myobj.save("audio.mp3")
#run it
os.system("mpg321 audio.mp3")
