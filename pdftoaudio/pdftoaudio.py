#importing required module
import PyPDF2
from gtts import gTTS
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename()
print(os.path.basename(filename))
#create a file obj and open in read binary mode
pdfFileObj = open(filename,'rb')     #'rb' for read binary mode
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
