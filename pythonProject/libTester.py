from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\tessdata'

dir = os.getcwd()+"\img"
print(dir)
im = Image.open(dir+"\mem_list.png")

text = pytesseract.image_to_string(im, lang = 'eng')

print(text)