import numpy as np

def compress_quadtree(img, threshold=10, max_depth=8):
    """Comprime una imagen en escala de grises (2D numpy uint8).
    Devuelve una lista de nodos hoja: (x, y, size, mean_value).
    - img: imagen cuadrada, lado potencia de 2.
    - threshold: diferencia máxima (max-min) para considerar la región uniforme.
    - max_depth: profundidad máxima para detener la subdivisión.
    """
    h, w = img.shape
    if h != w or (h & (h - 1)) != 0:
        raise ValueError("La imagen debe ser cuadrada y de tamaño potencia de 2 (p.ej. 256x256).")

    leaves = []

    def recurse(x, y, size, depth):
        region = img[y:y+size, x:x+size]
        minv = int(region.min())
        maxv = int(region.max())
        if (maxv - minv) <= threshold or size == 1 or depth >= max_depth:
            mean = int(region.mean())
            leaves.append((x, y, size, mean))
        else:
            hs = size // 2
            recurse(x, y, hs, depth + 1)            # top-left
            recurse(x + hs, y, hs, depth + 1)       # top-right
            recurse(x, y + hs, hs, depth + 1)       # bottom-left
            recurse(x + hs, y + hs, hs, depth + 1)  # bottom-right

    recurse(0, 0, h, 0)
    return leaves

def reconstruct_from_leaves(leaves, size):
    """Reconstruye una imagen (size x size) a partir de la lista de hojas.
    Cada hoja rellena su región con el valor medio (quantizado).
    """
    img = np.zeros((size, size), dtype=np.uint8)
    for x, y, s, mean in leaves:
        img[y:y+s, x:x+s] = np.uint8(mean)
    return img
