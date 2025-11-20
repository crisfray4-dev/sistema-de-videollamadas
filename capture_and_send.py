import cv2
import numpy as np
import socket
import time
import argparse

from quadtree import compress_quadtree, reconstruct_from_leaves
from rle import rle_encode_to_bytes
from utils import send_msg

def prepare_frame(frame, size):
    # Convertir a gris y redimensionar al tamaño deseado (cuadrado)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(gray, (size, size), interpolation=cv2.INTER_AREA)
    return img

def pack_frame(img, threshold, max_depth):
    # Comprime con quadtree y reconstruye la versión 'quantizada'
    leaves = compress_quadtree(img, threshold=threshold, max_depth=max_depth)
    recon = reconstruct_from_leaves(leaves, img.shape[0])
    flat = recon.flatten()
    payload = rle_encode_to_bytes(flat)
    return payload, len(flat)

def main(host, port, size, threshold, max_depth, camera_index):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Conectando a {host}:{port} ...")
    sock.connect((host, port))
    cap = cv2.VideoCapture(camera_index)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("No se pudo leer frame de la cámara.")
                break
            img = prepare_frame(frame, size)
            payload, orig_len = pack_frame(img, threshold, max_depth)
            send_msg(sock, payload)
            # muestra vista local (previsualización)
            cv2.imshow('Local (preview)', cv2.resize(img, (400, 400)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        sock.close()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5001)
    parser.add_argument('--size', type=int, default=256)
    parser.add_argument('--threshold', type=int, default=10)
    parser.add_argument('--max_depth', type=int, default=6)
    parser.add_argument('--camera', type=int, default=0)
    args = parser.parse_args()
    main(args.host, args.port, args.size, args.threshold, args.max_depth, args.camera)
