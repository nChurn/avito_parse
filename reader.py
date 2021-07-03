import base64
import io
import pytesseract
from PIL import Image


#img = Image.open('a.png')
#text = pytesseract.image_to_string(img)

#print(text)

def read_phone_number(base):
    base = base.split('64,')[-1].strip()

    pic = io.StringIO()
    image_string = io.BytesIO(base64.b64decode(base))
    image = Image.open(image_string)
    print(image)
    
    return pytesseract.image_to_string(image)

#image = open('a.png', 'rb').read()

#print(image)
#base = base64.b64encode(image)
#print(base)