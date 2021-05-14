import threading,socket,pygame
IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
class Client:
    def __init__(self):
        self.addr = (IP,PORT)
        self.conn  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self):
        try:
            self.conn.connect(self.addr)
            self.msgthread = threading.Thread(target=messagehandler)
        except Exception as e:
            pass
    def messagehandler(self):
        while True:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(msg)
    def send(self,msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' '*(HEADER-len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)
        
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)


def redrawWindow(win,player):
    win.fill((255,255,255))
    player.draw(win)
    pygame.display.update()


def main():
    c = Client()
    c.connect()
    run = True
    p = Player(50,50,100,100,(0,255,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p)

main()
