import socket,threading,time,datetime

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
HEADER = 64
FORMAT = "utf-8"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
DISCONNECT_MSG = "!DISCONNECT"
clients = set()
clients_lock = threading.Lock()
def log(logmsg):
    f = open("serverlogs.txt", "a")
    f.write(logmsg+"\n")
    f.close()
def getdatetime():
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return date
def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    date = getdatetime()
    log(f"[{date}] [NEW CONNECTION] {addr} connected.")
    connected = True
    with clients_lock:
        clients.add(conn)
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MSG:
                print(f"[DISCONNECT] {addr} disconnected.")
                date = getdatetime()
                log(f"[{date}] [DISCONNECT] {addr} disconnected.")
                print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
                connected = False
            else:
                print(f"[{addr}] {msg}")
                log(msg)
                with clients_lock:
                    for c in clients:
                        c.send(msg.encode(FORMAT))
    with clients_lock:
        clients.remove(conn)
        conn.close()
        
def start():
    server.listen()
    print(F"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
print("[STARTING] Server is starting...")
start()
