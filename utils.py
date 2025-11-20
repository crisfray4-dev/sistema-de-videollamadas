import struct

def send_msg(sock, data_bytes):
    """Envía un mensaje con prefijo de 4 bytes (uint32 big-endian) indicando la longitud."""
    length = len(data_bytes)
    sock.sendall(struct.pack('>I', length) + data_bytes)

def recv_exact(sock, n):
    """Recibe exactamente n bytes (bloquea hasta recibirlos o devuelve None si conexión cerrada)."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def recv_msg(sock):
    """Recibe un mensaje completo con el prefijo de 4 bytes. Devuelve bytes o None."""
    header = recv_exact(sock, 4)
    if not header:
        return None
    length = int.from_bytes(header, 'big')
    return recv_exact(sock, length)
