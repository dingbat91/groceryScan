import socket

def listenForCode(port:int):
    HOST = '0.0.0.0'
    PORT = port

    print(f"Starting server waiting for connection on {PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen()

        conn, addr = s.accept()
        with conn:
                print(f"Connection established with {addr}")
                data= conn.recv(1024)
                if data:
                    code = data.decode('utf-8')
                    print(f"Recieved:{code}")

if __name__ == "__main__":
     listenForCode(3225)