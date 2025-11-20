# Sistema de Videollamadas (Quadtrees + RLE) - Proyecto en Python

**Contenido**
- capture_and_send.py -> (sender) captura cámara, comprime (quadtree+RLE) y envía por TCP
- receive_and_display.py -> (receiver) escucha conexión TCP, recibe, decodifica y muestra
- quadtree.py -> funciones de compresión por quadtree y reconstrucción
- rle.py -> encode/decode RLE en bytes
- utils.py -> funciones de red (envío y recepción con prefijo de longitud)
- requirements.txt -> dependencias mínimas

## Requisitos
- Python 3.8+
- Instalar dependencias:
  ```
  pip install -r requirements.txt
  ```

## Uso (pruebas locales)
1. Abrir terminal A y ejecutar el receptor (escucha):
   ```
   python receive_and_display.py --port 5001
   ```
2. Abrir terminal B y ejecutar el emisor (envía desde la cámara):
   ```
   python capture_and_send.py --host 127.0.0.1 --port 5001
   ```

Pulsa `q` en la ventana de OpenCV para cerrar.

## Parámetros importantes
- `--size` : tamaño del frame cuadrado (p.ej. 256). Debe ser potencia de 2.
- `--threshold` : tolerancia (0-255). Mayor valor => más compresión (más pérdida).
- `--max_depth` : profundidad máxima del quadtree.
- `--camera` : índice de la cámara (0,1,...)

## Notas
- Este es un prototipo educativo: la transmisión usa TCP y un simple framing; en producción usarías WebRTC o protocolos adaptados.
- Si ejecutas en dos máquinas, sustituye `127.0.0.1` por la IP del receptor y asegúrate de abrir el puerto.
