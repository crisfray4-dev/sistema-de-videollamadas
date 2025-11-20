import cv2
import numpy as np
import socket
import argparse

from utils import recv_msg
from rle import rle_decode_from_bytes

def main(listen_host, listen_port, size):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((listen_host, listen_port))
    srv.listen(1)
    print(f"Escuchando en {listen_host}:{listen_port} ...")
    conn, addr = srv.accept()
    print("Conexión desde:", addr)
    try:
        while True:
            data = recv_msg(conn)
            if data is None:
                print("Conexión cerrada por el emisor.")
                break
            arr = rle_decode_from_bytes(data)
            img = arr.reshape((size, size))
            cv2.imshow('Remoto (recibido)', cv2.resize(img, (600, 600)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        conn.close()
        srv.close()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5001)
    parser.add_argument('--size', type=int, default=256)
    args = parser.parse_args()
    main(args.host, args.port, args.size)
