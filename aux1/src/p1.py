"""
Pregunta 1.
Pablo Pizarro @ppizarror / CC3501, 2019-1.
"""

# Obtiene la librería
from ex_color_palette import *

# Carga la imagen original
originalImage = mpl.imread("santiago.png")

# Obtiene una imagen indexada y su paleta de colores, este indizado indica a que posición de la paleta pertenece
# cada uno de los pixeles de la imagen
indexedImage, colorPalette = getColorPalette(originalImage)
print(colorPalette)

# Para el blanco y negro se promedian las componentes
newPalette = []
for i in range(len(colorPalette)):
    bgcolor = np.mean(colorPalette[i])
    newColor = np.array([bgcolor, bgcolor, bgcolor], dtype=np.float)
    newPalette += [newColor]
print(newPalette)

# Reconstruye la imagen
reconstructedImage = assignColors(indexedImage, newPalette)

# Crea el plot
fig, axs = mpl.subplots(2, 1)
axs[0].imshow(originalImage)
axs[1].imshow(reconstructedImage)
fig.suptitle('Imagen original y B/N')

# Muestra la figura
mpl.show()
