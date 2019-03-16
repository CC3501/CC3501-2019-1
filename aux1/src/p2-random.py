"""
Pregunta 2, colores random.
Pablo Pizarro @ppizarror / CC3501, 2019-1.
"""

# Obtiene la librería
from ex_color_palette import *

# Carga la imagen original
originalImage = mpl.imread("santiago.png")

# Obtiene una imagen indexada y su paleta de colores, este indizado indica a que posición de la paleta pertenece
# cada uno de los pixeles de la imagen
indexedImage, colorPalette = getColorPalette(originalImage)

# Creamos los colores límite v1, v2, v3
v1 = 0.25
v2 = 0.5
v3 = 0.6

# Creamos los colores entre esos límites
color_0 = np.random.rand(1, 3)
color_1 = np.random.rand(1, 3)
color_2 = np.random.rand(1, 3)
color_3 = np.random.rand(1, 3)

# Para el blanco y negro se promedian las componentes
newPalette = []
for i in range(len(colorPalette)):
    bgcolor = np.mean(colorPalette[i])
    if bgcolor < v1:
        color = color_0
    elif v1 < bgcolor < v2:
        color = color_1
    elif v2 < bgcolor < v3:
        color = color_2
    else:
        color = color_3
    newPalette += [color]

# Reconstruye la imagen
reconstructedImage = assignColors(indexedImage, newPalette)

# Crea el plot
fig, axs = mpl.subplots(2, 1)
axs[0].imshow(originalImage)
axs[1].imshow(reconstructedImage)
fig.suptitle('Imagen original y con nueva paleta')

# Muestra la figura
mpl.show()
