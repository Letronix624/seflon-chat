#!/bin/python3
import socket, threading, time, os, sys, tkinter, tkinter.simpledialog, tkinter.colorchooser, tkinter.messagebox, tkinter.ttk, json, tkinter.filedialog, tarfile, io, tkinter.dnd
from PIL import Image
from pygame import mixer
mixer.init()
print("!USER (username) to change username, !D to disconnect.")
port = 7777
try:
    ip = socket.gethostbyname("seflon.ddns.net")
except:
    tkinter.messagebox.showerror("Server closed", "The seflon.ddns.net server is not online.")
    print("Server is offline.")
    os._exit(0)
head = 1024
tf = "utf-8"
ff = "Calibri"
pydir = os.path.dirname(os.path.realpath(__file__))
username = "Client"
server = (ip, port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
messagehistory = []
historylength = 0
failedmessages = []
settingsfilename = "settings.json"
fileconfirmationopen = False
previewimages = []
appdata = ""
tempdir = ""
response = False
filetranster = False
if sys.platform == "win32":
    os.system(f"title {username}")
    appdata = f"{os.environ['APPDATA']}\\letsoftware\\seflonchat\\"
    tempdir = f"{os.environ['APPDATA']}\\letsoftware\\seflonchat\\temp\\"
    if not os.path.exists(appdata):
        os.makedirs(appdata)
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)
elif sys.platform == "linux":
    appdata = f"{os.environ['HOME']}/.letsoftware/seflonchat/"
    tempdir = f"{os.environ['HOME']}/.letsoftware/seflonchat/temp/"
    if not os.path.exists(appdata):
        os.makedirs(appdata)
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)
try:
    with open(f"{appdata}{settingsfilename}", "r") as data:
        settings = json.loads(data.read())
except:
    with open(f"{appdata}{settingsfilename}", "w") as data:
        settings = {
            "bg": "#333350",
            "fg": "#d9c6fb"
        }
        data.write(json.dumps(settings))
bg = settings["bg"]
fg = settings["fg"]
try:
    client.connect(server)
except Exception as E:
    tkinter.messagebox.showerror("Server closed", "The seflon.ddns.net server is not online.")
    print("Server is offline.")
    os._exit(0)
def filled(message, encode=True):
    if encode:
        if not len(message.encode(tf)+b' '* (head - len(message.encode(tf)))) > head:return message.encode(tf)+b' '* (head - len(message.encode(tf)))
    else:
        if not len(message+b' '* (head - len(message))) > head:return message+b' '* (head - len(message))
def rootthread():
    global frame2, textcanvas, historylength, fileconfirmationcanvas, root, convas, donvas, chatframe
    def res():
        topmenu.place_configure(width=root.winfo_width())
        bottommenu.place_configure(y = root.winfo_height()-66,width=root.winfo_width())
        Entry.place_configure(x=root.winfo_width()*0.075, width=root.winfo_width()*0.8+1, y=bottommenu.winfo_height()*0.25, height=bottommenu.winfo_height()*0.5)
        sendbutton.place_configure(x=root.winfo_width()*0.875, y=bottommenu.winfo_height()*0.25, height=bottommenu.winfo_height()*0.5, width=root.winfo_width()*0.075)
        uploadbutton.place_configure(x=root.winfo_width()*0.05, y=bottommenu.winfo_height()*0.25, height=bottommenu.winfo_height()*0.5, width=root.winfo_width()*0.025)
        colourbutton.place_configure(height=topmenu.winfo_height()*0.9, width=topmenu.winfo_height()*0.9, y=topmenu.winfo_height()*0.05, x=root.winfo_width()*0.1-topmenu.winfo_height()*0.9/2)
        profilesettings.place_configure(height=topmenu.winfo_height()*0.9, width=topmenu.winfo_height()*0.9, y=topmenu.winfo_height()*0.05, x=root.winfo_width()*0.2-topmenu.winfo_height()*0.9/2)
        changeaccount.place_configure(height=topmenu.winfo_height()*0.9, width=topmenu.winfo_height()*0.9, y=topmenu.winfo_height()*0.05, x=root.winfo_width()*0.3-topmenu.winfo_height()*0.9/2)
        changeserver.place_configure(height=topmenu.winfo_height()*0.9, width=topmenu.winfo_height()*0.9, y=topmenu.winfo_height()*0.05, x=root.winfo_width()*0.4-topmenu.winfo_height()*0.9/2)
        if fileconfirmationopen:
            fileconfirmationcanvas.place_configure(x=root.winfo_width()*0.1, y=root.winfo_height()*0.2, width=root.winfo_width()*0.8, height=root.winfo_height()*0.6)
        chatframe.place_configure(x=0, y=60, width=root.winfo_width(), height=(root.winfo_height()-126))
        convas[0].place_configure(x=2,y=22,height=fileconfirmationcanvas.winfo_height()*0.5-4, width=fileconfirmationcanvas.winfo_width()-4)
        convas[1].place_configure(x=fileconfirmationcanvas.winfo_width()*0.1, y=fileconfirmationcanvas.winfo_height()*0.7, height=fileconfirmationcanvas.winfo_height()*0.2, width=fileconfirmationcanvas.winfo_width()*0.3)
        convas[2].place_configure(x=fileconfirmationcanvas.winfo_width()*0.6, y=fileconfirmationcanvas.winfo_height()*0.7, height=fileconfirmationcanvas.winfo_height()*0.2, width=fileconfirmationcanvas.winfo_width()*0.3)
        donvas[0].place_configure(x=0, width=root.winfo_width(), height=60) #main canvas
        donvas[1].place_configure(y=30, x=root.winfo_width()*0.01, width=root.winfo_width()*0.98, height=25) #empty loading bar canvas
        donvas[2].place_configure(x=0, y=0, height=25) #loading bar filling percentage label
        donvas[3].place_configure(x=2, width=root.winfo_width()-4, y=2,height=28) #status label
    def changename():
        a = tkinter.simpledialog.askstring("Change Name", "New Name")
        if a:
            if not filetranster:
                client.send(filled(f"!USER {a}"))
    def colourchosen():
        def doit():
            global bg, fg
            topmenu.config(bg=bg, highlightbackground=fg)
            bottommenu.config(bg=bg, highlightbackground=fg, highlightcolor=fg)
            fileconfirmationcanvas.config(bg=bg, highlightbackground=fg, highlightcolor=fg)
            root.config(bg=fg)
            sendbutton.config(bg=bg, fg=fg, highlightbackground=fg)
            Entry.config(bg=bg, fg=fg, highlightbackground=fg, highlightcolor=fg)
            colourbutton.config(bg=fg, fg=bg, highlightbackground=bg)
            profilesettings.config(bg=fg, fg=bg, highlightbackground=bg)
            changeaccount.config(bg=fg, fg=bg, highlightbackground=bg)
            changeserver.config(bg=fg, fg=bg, highlightbackground=bg)
            textcanvas.config(bg=bg)
            frame2.config(bg=bg)
            uploadbutton.config(fg=fg, bg=bg, highlightbackground=fg)
            convas[0].config(bg=bg, fg=fg, highlightbackground=bg)
            convas[1].config(bg=bg, fg=fg, highlightbackground=fg)
            convas[2].config(bg=bg, fg=fg, highlightbackground=fg)
            donvas[0].config(background=bg, highlightcolor=fg, highlightbackground=fg)
            donvas[1].config(background=bg, highlightcolor=fg, highlightbackground=fg)
            donvas[2].config(background=fg, fg=bg, highlightcolor=fg, highlightbackground=fg)
            donvas[3].config(background=bg, fg=fg, highlightcolor=bg, highlightbackground=bg)
            for item in messagehistory:
                try:
                    item.config(bg=bg, fg=fg, highlightbackground=fg)
                except:
                    try:
                        item.config(bg=bg, highlightbackground=fg)
                    except:print(item)
        def primary():
            global bg
            a = tkinter.colorchooser.askcolor(bg)
            if a[1]:
                bg = a[1]
                colortop.destroy()
                doit()
                savesettings()
        def secondary():
            global fg
            a = tkinter.colorchooser.askcolor(fg)
            if a[1]:
                fg = a[1]
                colortop.destroy()
                doit()
                savesettings()
        global bg, fg
        colortop = tkinter.Toplevel()
        colortop.resizable(False, False)
        colortop.geometry("450x200")
        colortop.config(bg=bg)
        tkinter.Label(colortop, text="Change colour", font=("calibri", 20), bg=bg, fg=fg).pack(pady=10)
        tkinter.Button(colortop, text="Primary", bg=bg, fg=fg, font=("calibri", 20),command=primary, border=0).pack(pady=10)
        tkinter.Button(colortop, text="Secondary", bg=fg, fg=bg, font=("calibri", 20),command=secondary, border=0).pack(pady=10)
    def accountchange():
        a = tkinter.simpledialog.askstring("Change Account", "Username:")
        if a:
            if not filetranster:
                client.send(filled(f"!LOGIN {a}"))
    def connecttoserver():
        global server, client
        a = tkinter.simpledialog.askstring("Connect to server", "DNS or IP")
        if a:
            port = tkinter.simpledialog.askinteger("Connect to server", "Port")
            try:
                ip = socket.gethostbyname(a)
            except:
                ip = a
            server = (ip, port)
            client.send(filled("!D"))
            client.close()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect(server)
            except Exception as E:
                tkinter.messagebox.showerror(E, f"There was an error connecting to the Server.\nInfo: {E}\nConnecting back to seflon.ddns.net.")
                server = (socket.gethostbyname("seflon.ddns.net"), 7777)
                try:
                    client.connect(server)
                except:
                    tkinter.messagebox.showerror("Server closed", "The seflon.ddns.net server is not online.")
                    os._exit(0)
            client.send(filled(f"!LOGIN {socket.gethostname()}"))
    def send():
        message = Entry.get()
        Entry.delete(0, tkinter.END)
        sendmessage(message)
    def savesettings():
        settings["bg"] = bg
        settings["fg"] = fg
        with open(f"{appdata}{settingsfilename}", "w") as data:
            data.write(json.dumps(settings))
    def hideconvas():
        global fileconfirmationopen
        fileconfirmationopen = False
        fileconfirmationcanvas.place_forget()
    root = tkinterDnD.Tk()
    root.geometry('800x600')
    root.minsize(800,600)
    root.title("Seflon Chat")
    root.config(bg=fg)
    chatframe = tkinter.Frame(root)
    donvas = [
        tkinter.Canvas(root, background=bg, highlightcolor=fg, highlightbackground=fg, highlightthickness=2),
    ]
    donvas.append(tkinter.Canvas(donvas[0], background=bg, highlightcolor=fg, highlightbackground=fg, highlightthickness=2))
    donvas.append(tkinter.Label(donvas[1], background=fg, fg=bg,highlightcolor=fg, highlightbackground=fg, font=(ff, 15), text="123%", justify=tkinter.RIGHT))
    donvas.append(tkinter.Label(donvas[0], background=bg, fg=fg, highlightcolor=bg, highlightbackground=bg, font=(ff, 15), text="Downloading FILE_NAME", justify=tkinter.CENTER))
    topmenu = tkinter.Canvas(root, background=bg, highlightcolor=fg, highlightbackground=fg, highlightthickness=2)
    bottommenu = tkinter.Canvas(root, background=bg, highlightcolor=fg, highlightbackground=fg, highlightthickness=2)
    Entry = tkinter.Entry(bottommenu, fg=fg, bg=bg, font=("calibri", 15), highlightbackground=fg, highlightcolor=fg, highlightthickness=2)
    sendbutton = tkinter.Button(bottommenu, text="Send", font=(("calibri", 15)), command=send, bg=bg, fg=fg, borderwidth=0, highlightbackground=fg, highlightthickness=2)
    uploadbutton = tkinter.Button(bottommenu, text="F", font=(ff, 15), borderwidth=0, bg=bg, fg=fg, highlightbackground=fg, command=lambda:confirmsharefile(tkinter.filedialog.askopenfilename(title="Send file to chat")))

    colourbutton = tkinter.Button(topmenu, text="C", font=(("calibri", 15)), command=colourchosen, bg=fg, fg=bg, borderwidth=0, highlightbackground=bg)
    profilesettings = tkinter.Button(topmenu, text="PS", font=(("calibri", 15)), command=changename, bg=fg, fg=bg, borderwidth=0, highlightbackground=bg)
    changeaccount = tkinter.Button(topmenu, text="A", font=(("calibri", 15)), command=accountchange, bg=fg, fg=bg, borderwidth=0, highlightbackground=bg)
    changeserver = tkinter.Button(topmenu, text="CS", font=(("calibri", 15)), command=connecttoserver, bg=fg, fg=bg, borderwidth=0, highlightbackground=bg)
    textcanvas = tkinter.Canvas(chatframe, bg=bg, highlightthickness=0)
    textcanvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
    scrollbar = tkinter.ttk.Scrollbar(chatframe, orient=tkinter.VERTICAL, command=textcanvas.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    textcanvas.configure(yscrollcommand=scrollbar.set)
    textcanvas.bind("<Configure>", lambda e: textcanvas.configure(scrollregion=textcanvas.bbox("all")))
    frame2 = tkinter.Frame(textcanvas, bg=bg)
    textcanvas.create_window((0,0), window=frame2, anchor=tkinter.NW)
    topmenu.place(height=60)
    bottommenu.place(height=66)
    fileconfirmationcanvas = tkinter.Canvas(root, background=bg, highlightbackground=fg, highlightthickness=2)
    convas = [
        tkinter.Label(fileconfirmationcanvas, bg=bg, fg=fg, highlightbackground=bg, justify=tkinter.CENTER, font=(ff, 15), text="Send File\nFILE_NAME"),
        tkinter.Button(fileconfirmationcanvas, bg=bg, fg=fg, highlightbackground=fg, highlightthickness=2, font=(ff, 15), text="Send"),
        tkinter.Button(fileconfirmationcanvas, bg=bg, fg=fg, highlightbackground=fg, highlightthickness=2, font=(ff, 15), text="Cancel", command=hideconvas)
    ]
    Entry.place()
    sendbutton.place()
    uploadbutton.place()
    colourbutton.place()
    profilesettings.place()
    changeaccount.place()
    changeserver.place()
    chatframe.place()
    chatframe.register_drop_target("*")
    chatframe.bind("<<Drop>>", lambda x:confirmsharefile(x.data))

    root.bind("<Configure>", lambda x:res())
    root.bind("<Return>", lambda x: send())


    for message in failedmessages:
        displaymessageinchat(message)
    root.mainloop()
    try:
        client.send(filled("!D"))
    except:pass
    os._exit(0)
def sendmessage(msg):
    global filetranster, fileconfirmationopen
    if not filetranster:
        if msg.replace(" ", ''):
            if "!~" in msg:
                displaymessageinchat("No Permission")
            elif msg == "!f":
                confirmsharefile(tkinter.filedialog.askopenfilename(title="Send file to chat"))
            elif msg.startswith("!"):
                displaymessageinchat("[INFO] Unknown Command.")
            elif len(msg) < head:
                message = msg.strip()
                try:
                    client.send(filled(message))
                except:
                    displaymessageinchat("[INFO] Your message wasn't sent.")
            else:
                displaymessageinchat("[INFO] Your message wasn't sent.\nYour message is too long.")
        if msg == "!D":
            os._exit(0)
    else:
        displaymessageinchat("[INFO] Can't do that during file transfer.")
def recievemessage():
    global username, response, historylength, filetranster
    connected = True
    while connected:
        try:
            if not filetranster:
                message = client.recv(head).decode(tf).strip()
                if message:
                    if message == "!KICK":
                        connected = False
                    elif message.startswith("!USER "):
                        username = message[6:]
                    elif message == "!PING":
                        if not filetranster:
                            client.send(filled("!PING"))
                    elif message == "!~ok":
                        response = True
                    elif message.startswith("!~1"):
                        print("Initialized !~g filetransfer")
                        filetranster = True
                    elif message.startswith("!~f"):
                        finfo = message[3:].split("!~f")
                        if finfo[0].lower().endswith(".gif") or\
                            finfo[0].lower().endswith(".pgm") or\
                            finfo[0].lower().endswith(".ppm") or\
                            finfo[0].lower().endswith(".png") or\
                            finfo[0].lower().endswith(".gif") or\
                            finfo[0].lower().endswith(".jpg") or\
                            finfo[0].lower().endswith(".jpeg") or\
                            finfo[0].lower().endswith(".bmp") or\
                            finfo[0].lower().endswith(".jfif"):
                            print("about to print image")
                            filetranster = True
                            print("filetranster = True")
                            client.send(filled(f"!~gd{finfo[0]}"))
                            print("client.send(filled(f\"!~gd{finfo[0]}\"))")
                            finfo2 = client.recv(head).decode(tf)[2:]
                            print('finfo2 = client.recv(head).decode(tf)[2:]')
                            if finfo2[0] == "1":finfo2 = client.recv(head).decode(tf)[2:]
                            print("if finfo2[0] == \"1\":finfo2 = client.recv(head).decode(tf)[2:]")
                            filesize = int(finfo2[1:])
                            print("filesize = int(finfo2[1:])")
                            print("Loading image")
                            image = b''
                            while len(image) < filesize:
                                messageb = client.recv(head)
                                if messageb:
                                    image+=messageb
                                    print(f"{len(image)} - {filesize}")
                                else:print("recieving nothing")
                            print("through")
                            image = image[:-(len(image)-filesize)]
                            print("image = image[:-(len(image)-filesize)]")
                            filetranster = False
                            print("filetranster = False")
                            client.send(filled("!PING"))
                            print("client.send(filled(\"!PING\"))")
                            pilimage = Image.open(io.BytesIO(image))
                            print("opened. now trying to make it TK")
                            pilmage = ImageTk.PhotoImage(pilimage)
                            print("good. appending:")
                            previewimages.append(pilmage)
                            print("previewimages.append(ImageTk.PhotoImage(pilmase))")
                            if len(previewimages) > 50:
                                previewimages[0].pop()
                            print("Image loaded")
                            if historylength >= 300:
                                for item in range(int(round(len(messagehistory)/2))):
                                    try:messagehistory[0].destroy()
                                    except:pass
                                    messagehistory.pop(0)
                                historylength = len(messagehistory)
                            else:
                                historylength += 1
                            messagehistory.append(tkinter.Canvas(frame2, bg=bg, highlightbackground=fg, highlightthickness=2))
                            messagehistory.append(tkinter.Label(messagehistory[-1], text=f"{finfo[1]} sent an image:\n{finfo[0]} {round(float(finfo[2])/100000)/10}MB", bg=bg, fg=fg, font=("calibri", 15), justify=tkinter.LEFT, highlightbackground=bg))
                            messagehistory[-1].pack(side=tkinter.TOP, anchor=tkinter.N, padx=2, pady=2)
                            print("about to show")
                            tkinter.Label(messagehistory[-2], image=previewimages[-1]).pack(side="top", anchor="n", padx=2, pady=2)
                            print("bam")
                            messagehistory.append(tkinter.Button(messagehistory[-2], text="Download", bg=bg, fg=fg, border=0, highlightbackground=fg, highlightcolor="white", highlightthickness=2,font=("calibri", 15), command=lambda:download(finfo[0])))
                            messagehistory[-1].pack(side=tkinter.TOP, anchor=tkinter.N, pady=10, padx=10)
                            messagehistory[-3].pack(side=tkinter.TOP, anchor=tkinter.NW, pady=5, expand=True)
                            time.sleep(0.01)
                            textcanvas.configure(scrollregion=textcanvas.bbox("all"))
                            textcanvas.yview_moveto('1.0')
                            print("through")
                            client.send(filled("!PING"))
                        #elif finfo[0].lower().endswith(".mp3") or\
                        #    finfo[0].lower().endswith(".ogg") or\
                        #    finfo[0].lower().endswith(".wav") or\
                        #    finfo[0].lower().endswith(".mod") or\
                        #    finfo[0].lower().endswith(".xm"):
                        #    pass
                        else:
                            if historylength >= 300:
                                for item in range(int(round(len(messagehistory)/2))):
                                    try:messagehistory[0].destroy()
                                    except:pass
                                    messagehistory.pop(0)
                                historylength = len(messagehistory)
                            else:
                                historylength += 1
                            messagehistory.append(tkinter.Canvas(frame2, bg=bg, highlightbackground=fg, highlightthickness=2))
                            messagehistory.append(tkinter.Label(messagehistory[-1], text=f"{finfo[1]} sent a file:\n{finfo[0]} {round(float(finfo[2])/100000)/10}MB", bg=bg, fg=fg, font=("calibri", 15), justify=tkinter.LEFT, highlightbackground=bg))
                            messagehistory[-1].pack(side=tkinter.TOP, anchor=tkinter.N, padx=2, pady=2)
                            messagehistory.append(tkinter.Button(messagehistory[-2], text="Download", bg=bg, fg=fg, border=0, highlightbackground=fg, highlightcolor="white", highlightthickness=2,font=("calibri", 15), command=lambda:download(finfo[0])))
                            messagehistory[-1].pack(side=tkinter.TOP, anchor=tkinter.N, pady=10, padx=10)
                            messagehistory[-3].pack(side=tkinter.TOP, anchor=tkinter.NW, pady=5, expand=True)
                            time.sleep(0.01)
                            textcanvas.configure(scrollregion=textcanvas.bbox("all"))
                            textcanvas.yview_moveto('1.0')
                    elif message.startswith("!msg"):
                        tkinter.messagebox.showinfo("Message from Server",message[4:])
                    elif "!~" in message:
                        pass
                    else:
                        displaymessageinchat(message)
            else:time.sleep(1)
        except:pass
    client.send(filled("!D"))
    os._exit(0)
def displaymessageinchat(message):
    global historylength
    try:
        if historylength >= 300:
            for item in range(int(round(len(messagehistory)/2))):
                try:messagehistory[0].destroy()
                except:pass
                messagehistory.pop(0)
            historylength = len(messagehistory)
        else:
            historylength += 1
        messagehistory.append(tkinter.Label(frame2, text=message, bg=bg, fg=fg, font=("calibri", 15), justify=tkinter.LEFT, highlightbackground=fg, highlightthickness=2))
        messagehistory[-1].pack(side=tkinter.TOP, anchor=tkinter.NW, pady=5, expand=True)
        #tkinter.Label(frame2).pack()
        time.sleep(0.01)
        textcanvas.configure(scrollregion=textcanvas.bbox("all"))
        textcanvas.yview_moveto('1.0')
    except:failedmessages.append(message)
def confirmsharefile(filedirectory):
    global fileconfirmationopen
    if type(filedirectory) == str:
        if filedirectory.startswith("{"):
            filedirectory = filedirectory[1:-1]
        if filedirectory:
            fileconfirmationopen = True
            fileconfirmationcanvas.place_configure(x=root.winfo_width()*0.1, y=root.winfo_height()*0.2, width=root.winfo_width()*0.8, height=root.winfo_height()*0.6)
            convas[0].config(text=f"Send File\n{os.path.basename(filedirectory)}")
            convas[1].config(command=lambda:sharefile(filedirectory))
def sharefile(filedirectory):#send file
    global fileconfirmationopen
    fileconfirmationopen = False
    fileconfirmationcanvas.place_forget()
    if filedirectory:
        if os.path.getsize(filedirectory) < 1000000000:
            displaymessageinchat(f"Sending {os.path.basename(filedirectory)}")
            filename = os.path.basename(filedirectory)
            with tarfile.open(os.path.join(tempdir, filename), "w:bz2") as file:
                file.add(filedirectory, arcname=filename)
            client.send(filled(f"!~f{os.path.basename(filedirectory)}!~f{os.path.getsize(os.path.join(tempdir, filename))}"))
            def sendingthread():
                global response, filetranster, historylength
                filetranster = True
                while 1:
                    if response:
                        response = False
                        print('opening '+ filedirectory)
                        data = open(os.path.join(tempdir, filename), "rb")
                        print("opened")
                        sentnumber = 0
                        filesize = (os.path.getsize(os.path.join(tempdir, filename)) - os.path.getsize(os.path.join(tempdir, filename)) % head) + head
                        if historylength >= 300:
                            for item in range(int(round(len(messagehistory)/2))):
                                try:messagehistory[0].destroy()
                                except:pass
                                messagehistory.pop(0)
                            historylength = len(messagehistory)
                        else:
                            historylength += 1
                        messagehistory.append(tkinter.Canvas(frame2, bg=bg, highlightbackground=fg, highlightthickness=2))
                        messagehistory.append(tkinter.Label(messagehistory[-1], bg=bg, padx=252, pady=3))
                        messagehistory.append(tkinter.Label(messagehistory[-2], text="0%", bg=bg, fg=fg, font=("calibri", 15), justify=tkinter.LEFT))
                        messagehistory.append(tkinter.Canvas(messagehistory[-3], bg=bg, highlightbackground=fg, highlightthickness=2))
                        messagehistory.append(tkinter.Canvas(messagehistory[-1], bg=fg, highlightbackground=fg, highlightthickness=10))
                        messagehistory[-4].pack(padx=2, pady=2)
                        messagehistory[-2].place(x=105, height=20, y=5, width=400)
                        messagehistory[-1].place(height=20, width=0, x=0, y=0)
                        messagehistory[-3].place(x=5, y=5, width=100, height=20)
                        messagehistory[-5].pack(side=tkinter.TOP, anchor=tkinter.NW, pady=5,expand=True)
                        progress = [messagehistory[-1], messagehistory[-2], messagehistory[-3], messagehistory[-4], messagehistory[-5]]
                        time.sleep(0.01)
                        textcanvas.configure(scrollregion=textcanvas.bbox("all"))
                        textcanvas.yview_moveto('1.0')
                        while True:
                            message = data.read(head)
                            if message:
                                client.sendall(filled(message, False))
                                sentnumber += head
                                progress[2].config(text=f"{float(round(sentnumber/filesize*1000))/10}%")
                                progress[0].place_configure(width=round(sentnumber/filesize*400))
                            else:
                                print("Sent All")
                                for item in progress:
                                    try:
                                        item.destroy()
                                        messagehistory.pop(-1)
                                    except:print("boom")
                                filetranster = False
                                client.send(filled("!~done"))
                                break
                        client.send(filled("!PING"))
                        data.close()
                        break
            threading.Thread(target=sendingthread).start()
        else:
            displaymessageinchat("File too big to send.")
def download(filename):#recieve file
    filepath = tkinter.filedialog.asksaveasfilename(title=f"Save {filename}", initialfile=filename)
    def main():
        global filetranster
        filetranster = True
        localfilename = os.path.basename(filepath)
        localfiledirectory = os.path.dirname(filepath)
        donvas[3].config(text=f"Downloading {filename}")
        donvas[2].place_configure(width=0)
        donvas[2].config(text="0%")
        for i in range(58):
            donvas[0].place_configure(y=i)
            chatframe.place_configure(x=0, y=60+i, width=root.winfo_width(), height=(root.winfo_height()-126-i))
            textcanvas.configure(scrollregion=textcanvas.bbox("all"))
            time.sleep(0.01)
        client.send(filled(f"!~g {filename}"))
        finfo = client.recv(head).decode(tf)[2:]
        if finfo[0] == "1":finfo = client.recv(head).decode(tf)[2:]
        filesize = int(finfo[1:])
        recieved = b''
        while len(recieved) < filesize:
            messageb = client.recv(head)
            if messageb:
                recieved+=messageb
                recievedlen = len(recieved)
                donvas[2].place_configure(width=round(donvas[1].winfo_width()*(recievedlen/filesize)))
                donvas[2].config(text=f"{round(recievedlen/filesize*100)}%")
            else:break
        recieved = recieved[:-(len(recieved)-filesize)]
        with open(os.path.join(tempdir,localfilename), "wb") as file:file.write(recieved)
        del recieved
        try:
            with tarfile.open(os.path.join(tempdir, localfilename), "r:bz2") as data:
                data.extract(localfilename, path=localfiledirectory)
        except Exception as E:
            print(f"Recieved object not bz2. {E}")
            with open(os.path.join(tempdir,localfilename), "rb") as data:
                with open(filepath, "wb") as file:file.write(data.read())
        filetranster = False
        displaymessageinchat(f"Downloaded {filename}")
        for i in range(58):
            donvas[2].place_configure(width=round(donvas[1].winfo_width()-donvas[1].winfo_width()*(i/58)))
            donvas[2].config(text=f"{round((58-i)/58*100)}%")
            donvas[0].place_configure(y=58-i)
            chatframe.place_configure(x=0, y=60+58-i, width=root.winfo_width(), height=(root.winfo_height()-126+58-i))
            time.sleep(0.01)
        textcanvas.configure(scrollregion=textcanvas.bbox("all"))
        textcanvas.yview_moveto('1.0')
    threading.Thread(target=main).start()
if __name__ == "__main__":
    threading.Thread(target=rootthread).start()
    threading.Thread(target=recievemessage).start()
    client.send(filled(f"!LOGIN {socket.gethostname()}"))