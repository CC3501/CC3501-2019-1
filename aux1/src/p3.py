"""
Pregunta 3.
Pablo Pizarro @ppizarror / CC3501, 2019-1.
"""

# Obtiene la librería
from ex_color_palette import *

# Carga la imagen original
originalImage = mpl.imread("santiago.png")

# Creamos una imagen doble, originalmente estará vacía
newImage = np.zeros(shape=(2 * originalImage.shape[0], 2 * originalImage.shape[1], 3), dtype=np.float)

# Se copian los pixeles conocidos cada 2x2
for i in range(originalImage.shape[0]):  # Fila
    for j in range(originalImage.shape[1]):  # Columna

        # Calcula los índices de cada bloque
        i2 = 2 * i - 1
        j2 = 2 * j - 1

        # Asigna los colores a cada sector
        newImage[i2, j2, :] = originalImage[i, j, :]
        newImage[i2 + 1, j2, :] = originalImage[i, j, :]
        newImage[i2, j2 + 1, :] = originalImage[i, j, :]
        newImage[i2 + 1, j2 + 1, :] = originalImage[i, j, :]

# Promedia los colores vecinos
newImageAvg = np.zeros(shape=newImage.shape, dtype=np.float)
for i in range(newImage.shape[0]):  # Fila
    for j in range(newImage.shape[1]):  # Columna

        # Si el pixel es posición par (o sea, entre medio) calcula
        # la suma promedio
        colorsum = np.zeros([1, 3])
        if (i % 2 == 0 or j % 2 == 0) and j < (newImage.shape[1] - 2) and i < (newImageAvg.shape[0] - 2):
            colorsum = np.add(colorsum, newImage[i - 1, j])  # Superior
            colorsum = np.add(colorsum, newImage[i + 1, j])  # Inferior
            colorsum = np.add(colorsum, newImage[i, j + 1])  # Derecha
            colorsum = np.add(colorsum, newImage[i, j - 1])  # Izquierda
            colorsum = np.add(colorsum, newImage[i - 1, j - 1])  # Sup izq
            colorsum = np.add(colorsum, newImage[i - 1, j + 1])  # Sup der
            colorsum = np.add(colorsum, newImage[i + 1, j - 1])  # Inf izq
            colorsum = np.add(colorsum, newImage[i + 1, j + 1])  # Inf der
            colorsum = np.divide(colorsum, 8)
        else:
            colorsum = newImage[i, j, :]

        # Asigna el color
        newImageAvg[i, j, :] = colorsum

# Muestra la figura
mpl.imshow(newImage)
mpl.savefig('p2-new-normal.png')

mpl.imshow(newImageAvg)
mpl.savefig('p2-new-avg.png')

mpl.show()
