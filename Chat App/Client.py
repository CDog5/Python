import socket,sys,threading,time,datetime
from tkinter import *
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
recmsg=""
username=""
messages=[]
def key(e):
    if(e.keysym == "Return"):
        if str(window.focus_get()) == ".!entry":
            login()
        elif str(window.focus_get()) == ".!entry2":
            chat()
def onclose():
    try:
        send(DISCONNECT_MSG)
        thread.join()
    except:
        pass
    tasklbl.set("Disconnected.")
    print("Disconnected.")
    time.sleep(2)
    window.destroy()
    sys.exit(0)
def login():
    username = str(usern.get())
    if username == "":
        return
    tasklbl.set("Logged in as '"+username+"'.")
    print("Logged in as '"+username+"'.")
    try:
        client.connect(ADDR)
        thread = threading.Thread(target=handlemessages)
        thread.start()
    except:
        tasklbl.set("Possible connection error.")
        print("Possible connection error.")
def handlemessages():
    while True:
        recmsg = client.recv(2048).decode(FORMAT)
        if recmsg:
            msg_list.insert(END, recmsg)
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
def chat():
    username = usern.get()
    userinput = chattxt.get()
    if userinput.lower() == "quit" or userinput.lower() == "exit":
        onclose()
    elif userinput != "":
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        send(f"[{date}] [{username}] {userinput}")
    time.sleep(0.1)
    chattxt.set("")


window = Tk()
msgtxt = StringVar()
window.geometry("500x500")
window.configure(bg='gray84')
window.title("Chat App")
window.resizable(height = False, width = False)
window.bind_all('<Key>', key)
usern = StringVar()
chattxt = StringVar()
tasklbl = StringVar()
lgbox = Entry(window,textvar=usern,width=30)
lgbox.place(x=250,y=15)
tsklbl = Label(window,textvar=tasklbl,background='gray84')
tsklbl.place(x=25,y=15)
usrnlbl = Label(window,text="Username:",background='gray84')
usrnlbl.place(x=185,y=15)

lgbutton = Button(window,text="Login",command=login,background='palegreen1',activebackground='palegreen1')
lgbutton.place(x=450,y=10)
messages_frame = Frame(window)
scrollbar = Scrollbar(messages_frame)
msg_list = Listbox(messages_frame, height=15, width=72, yscrollcommand=scrollbar.set)
scrollbar.config(command=msg_list.yview)

scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
messages_frame.pack()
messages_frame.place(x=25,y=100)
chatbox = Entry(window,textvar=chattxt,width=65)
chatbox.place(x=25,y=400)
chbutton = Button(window,text="Chat",command=chat,background='palegreen1',activebackground='palegreen1')
chbutton.place(x=435,y=395)
lbl = Label(window,text="Developed by Callum Sheppard in August 2020.",background='gray84')
lbl.place(x=25,y=450)
window.protocol("WM_DELETE_WINDOW", onclose)

window.mainloop()
