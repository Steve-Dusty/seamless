import socket

HOST = "127.0.0.1"
PORT = 8000

def recv_request(sock, ending=b"\r\n\r\n"):
    data = b""
    search_pos = 0
    while True:
        chunk = sock.recv(1)
        if not chunk:
            break
        if ord(chunk) == ending[search_pos]:
            search_pos += 1
            if search_pos == len(ending):
                break
        else:
            data += ending[:search_pos] + chunk
            search_pos = 0
    return data

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = recv_request(conn)

                request = data.decode('utf-8')
                lines = request.split('\r\n')
                url = lines[0].split()[1]
                method = lines[0].split()[0].upper()
                if method == "CONNECT":
                    # parsing everything 
                    try:
                        request_port = int(url.split(":")[1])
                    # make port 80 for all URL without defined ports
                    except:
                        request_port = 80
                    
                    request_host = url.split(":")[0] 
                    print(f'Received URL: {request}')

                    # Open new socket
                    psocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    psocket.connect((request_host, request_port))
                    print("[CONNECTED] ==> Sending Request to Target")
                    
                    psocket.sendall(request.encode('utf-8'))
                    print("[SUCCESS] ==> Request sent to Target")

                    # retrieve target response
                    pdata = recv_request(psocket)
                    print("[SUCCESS] ==> Target response retrieved")

                    # send pdata back to conn (og client)
                    conn.sendall(pdata)
                    print(f"[FINISHED] ==> Data received {pdata}")
                    break

if __name__ == "__main__":
    main()
