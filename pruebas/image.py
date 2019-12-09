import matplotlib.pyplot as plt
from PIL import Image
import io
import numpy as np

#img = mpimg.imread('pokemons/135.png')
myfile = open("../pokemons/7.png", 'rb')
bytes = myfile.read()
size = len(bytes)
image = Image.open(io.BytesIO(bytes))
data = np.array(image)
plt.imshow(data)
plt.axis('off')
plt.show()
print(size)