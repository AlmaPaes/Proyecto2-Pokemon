import base64
from PIL import Image
import io
import matplotlib.pyplot as plt
import numpy as np

with open("pokemons/bulbasaur.png", "rb") as image_file:
    encoded_string_1 = base64.b64encode(image_file.read())
with open("pokemons/ninetales.png", "rb") as image_file:
    encoded_string_2 = base64.b64encode(image_file.read())

imgdata = base64.decodebytes(encoded_string_2)
image = Image.open(io.BytesIO(imgdata))
data = np.array(image)
plt.axis('off')
plt.imshow(data)
plt.show()

'''with open("bulbasaur2.png", "wb") as fh:
    fh.write(base64.decodebytes(encoded_string_1))
with open("ninetales2.png", "wb") as fh:
    fh.write(base64.decodebytes(encoded_string_2))'''





