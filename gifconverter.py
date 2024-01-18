import tkinter as tk
import tkinter.ttk as ttk
import os
import re
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, ImageOps

class MyApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.flag = False
        self.count = 0

        main = tk.Frame(self.master)
        main.pack(expand=True, fill=tk.BOTH)
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self)

#top
        self.top = tk.Frame(main, height=300)
        self.top.pack(anchor=tk.N,expand=1, fill=tk.BOTH)
        self.previewframe = tk.LabelFrame(self.top, bg="#111111", width=250, height=250, labelanchor="n")
        self.previewframe.propagate(False)
        self.previewframe.place(x=10, y=10)
        self.previewname = tk.Label(self.top, text="名前")
        self.previewname.place(x=270,y=15)
        self.previewnamebox = tk.Entry(self.top, state="readonly")
        self.previewnamebox.place(x=270, y=40, width=240)
        self.sep1 = ttk.Separator(self.top)
        self.sep1.place(x=270, y=65, width=240)
        self.sep2 = ttk.Separator(self.top)
        self.sep2.place(x=270, y=65, width=240)
        self.topframe = tk.Label(self.top, text="フレーム数")
        self.topframe.place(x=270, y=70)
        vcmd = self.register(self.onlyint)
        self.topframebox = tk.Spinbox(self.top, from_=1, to=999, increment=1, command=self.spin_input, textvariable=tk.IntVar(value=1), validate="key", validatecommand=(vcmd, "%S"))
        self.topframebox.place(x=270, y=95)

#bot
        self.bot = ttk.Frame(main, height=250, relief="ridge")
        self.bot.propagate
        self.boteditor = ttk.Frame(main, height=250, width=100, relief="groove")
        self.boteditor.propagate(False)
        self.boteditor.pack(anchor=tk.SE, side=tk.RIGHT)
        self.bot.pack(anchor=tk.SW,fill="y", side=tk.BOTTOM)
        fpslist = (10,24,30,60)
        self.fpslabel = tk.Label(self.boteditor, text="fps数")
        self.fpslabel.grid(columnspan=2, row=0, pady=5)
        self.editfps = ttk.Combobox(self.boteditor,width=10, textvariable=tk.IntVar(), values=fpslist)
        self.editfps.set(10)
        self.editfps.grid(columnspan=2, row=1)
        self.editbefore = tk.Button(self.boteditor, text=" << ", command=lambda whitch="before": self.trickimage(whitch))
        self.editbefore.grid(column=0, row=2)
        self.editafter = tk.Button(self.boteditor, text=" >> ", command=lambda whitch="after": self.trickimage(whitch))
        self.editafter.grid(column=1, row=2)
        self.editor1 = tk.Button(self.boteditor, text=" ↶ ", command=lambda lr="left": self.rotateimage(lr))
        self.editor1.grid(column=0, row=3, padx=5, pady=10)
        self.editor2 = tk.Button(self.boteditor, text=" ↷ ", command=lambda lr="right":self.rotateimage(lr))
        self.editor2.grid(column=1, row=3, padx=5, pady=10)
        self.editor2 = tk.Button(self.boteditor, text="  ⇔  ", command=lambda lr="right":self.mirrorimage())
        self.editor2.grid(columnspan=2, row=4, padx=5, pady=10)
#menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        menu_file = tk.Menu(self, tearoff=0)
        menubar.add_cascade(label="ファイル", menu=menu_file)
        menu_file.add_command(label="新規プロジェクト")
        menu_file.add_command(label="ファイルを開く")
        menu_file.add_separator()
        menu_file.add_command(label="画像を開く", command=self.getimage_btn)
        menu_file.add_command(label="フォルダを開く")
        menu_file.add_separator()
        menu_file.add_command(label="名前を付けて保存", command=self.saveimage)
        menu_edit = tk.Menu(self, tearoff=0)
        menubar.add_cascade(label="編集", menu=menu_edit)
        menu_edit.add_command(label="選択画像を一つ前へ", command=lambda whitch="before": self.trickimage(whitch))
        menu_edit.add_command(label="選択画像を一つ後ろへ", command=lambda whitch="after": self.trickimage(whitch))
        menu_edit.add_separator()
        copy_command = lambda: self.copyimage()
        menu_edit.add_command(label="画像をコピー", command=copy_command)
        
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def onlyint(self, S):
        return re.match(re.compile("[0-9]*"), S) is not None
      
    def spin_input(self):
        select = int(str(self.select)[-1])

        value = self.topframebox.get()
        if not value.isdigit():
            tk.StringVar().set(1)

        change = self.topframebox.get()
        self.framelist[select].set(change)
        
    def clear_topimage(self):
        self.image_label.image = NotImplemented
        self.image_label.destroy()
        self.flag = False

    def scale_box(self,image,conv):
        w, h = image.size
        aspect = w / h
        if 1 >= aspect:
            newh = conv
            neww = round(newh * aspect)
        else:
            neww = conv
            newh = round(neww / aspect)
        dst = neww,newh
        return dst

    def getimage_top(self,num):
        image = self.piclist[num]
        name = self.namelist[num]
        frame = self.framelist[num].get()

        topsize = self.scale_box(image,250)

        retop = image.resize(topsize)
        topimage = ImageTk.PhotoImage(retop)

        self.image_label = tk.Label(self.previewframe, image=topimage)
        self.image_label.image = topimage
        self.image_label.pack()

        self.previewnamebox.configure(state="normal")
        self.previewnamebox.delete(0,tk.END)
        self.previewnamebox.insert(tk.END, name)
        self.previewnamebox.configure(state="readonly")

        self.topframebox.delete(0,tk.END)
        self.topframebox.insert(tk.END, frame)

        self.flag = True

    def getimage_bot(self,num):
        image = self.piclist[num]
        name = self.namelist[num]
        frame = self.framelist[num]

        botsize = self.scale_box(image,130)

        rebot = image.resize(botsize)
        botimage = ImageTk.PhotoImage(rebot)

        if 0 < num:
            self.bot.nametowidget(f"bot{num-1}").configure(relief="raised")
        self.botframe = ttk.Frame(self.bot, name=f"bot{num}", width=150, height=250, borderwidth=2, relief="sunken")
        self.botframe.propagate(False)
        self.botframe.pack(side=tk.LEFT)
        self.botimgnum = tk.Label(self.botframe, text=num)
        self.botimgnum.pack(pady=5)
        self.botpreviewframe = tk.LabelFrame(self.botframe,bg="#111111", width=130, height=130, labelanchor="n")
        self.botpreviewframe.propagate(False)
        self.botpreviewframe.pack(pady=5)
        self.botimage_label = tk.Label(self.botpreviewframe, name=f"botimg{num}", image=botimage)
        self.botimage_label.image = botimage
        self.botimage_label.pack()
        self.botimgname = tk.Label(self.botframe, name=f"botname{num}", text=name)
        self.botimgname.pack(anchor=tk.NW, padx=10, pady=5)
        self.botimglength = tk.Label(self.botframe, name=f"botlen{num}", textvariable=frame)
        self.botimglength.pack(anchor=tk.NW, padx=10, pady=5)

        self.botframe.bind("<Button-1>", lambda event,select=self.botframe,len=self.botimglength: self.select_image(event,select,len))
        self.botimgnum.bind("<Button-1>", lambda event,select=self.botframe,len=self.botimglength: self.select_image(event,select,len))
        self.botpreviewframe.bind("<Button-1>", lambda event,select=self.botframe,len=self.botimglength: self.select_image(event,select,len))
        self.botimage_label.bind("<Button-1>", lambda event,select=self.botframe,len=self.botimglength: self.select_image(event,select,len))
        self.botimgname.bind("<Button-1>", lambda event,select=self.botframe,len=self.botimglength: self.select_image(event,select,len))
        self.botimglength.bind("<Button-1>", lambda event,select=self.botframe,len=self.botimglength: self.select_image(event,select,len))

        self.select = self.botframe
        self.selectlen = self.botimglength

    def insert_bot(self,num):
        select = num
        gap = self.count - select
        i = 0
        while  i < gap:
            self.getimage_bot(self.count)
            
            i = i + 1

    def getimage_btn(self):
        print("getimage_btn")
        type = [("画像ファイル","*.jpg;*.jpeg;*.png;*.bmp")]
        paths = filedialog.askopenfilenames(filetypes=type)
        if paths == "":
            return "break"
        for imgpath in paths:
            self.name = os.path.basename(imgpath)
            print(self.flag)
            if self.flag == True:
                self.clear_topimage()
                self.select.configure(relief="raised")
            if self.count == 0: #一度目の追加
                self.selectnum = 0
                self.pathlist = [imgpath]
                self.piclist = [Image.open(imgpath)]
                self.namelist = [self.name]
                self.framelist = [tk.IntVar(value=1)]
                size = self.piclist[0].size
                self.getimage_top(self.count)
                self.getimage_bot(self.count)
                self.selectnum = self.selectnum + 1
            elif self.selectnum == 0: #最初に追加
                print("insert")
            elif self.count == self.selectnum: #最後に追加
                self.pathlist.append(imgpath)
                pic = Image.open(imgpath)
                size = self.piclist[0].size
                self.piclist.append(pic.resize(size))
                self.namelist.append(self.name)
                self.framelist.append(tk.IntVar(value=1))
                self.getimage_top(self.count)
                self.getimage_bot(self.count)
                self.selectnum = self.selectnum + 1
#            else: #途中に追加
#                self.pathlist.insert(self.selectnum,imgpath)
#                pic = Image.open(imgpath)
#                size = self.piclist[0].size
#                self.piclist.insert(self.selectnum,pic.resize(size))
#                self.namelist.insert(self.selectnum,self.name)
#                self.framelist.insert(self.selectnum,tk.IntVar(value=1))
#                self.getimage_top(self.selectnum)
#                self.getimage_bot(self.selectnum)
#                self.botframe.configure(relief="sunken")
#                print(self.namelist)
#                self.selectnum + 1

            self.count = self.count + 1
            self.flag = True

    def select_image(self,event,select,len):
        self.select.configure(relief="raised")
        self.selectnum = int(str(select)[-1])

        self.select = self.bot.nametowidget(select)
        self.select.configure(relief="sunken")

        self.selectlen = self.bot.nametowidget(len)

        self.clear_topimage()
        self.getimage_top(self.selectnum)

        self.flag = True

    def trickimage(self,whitch):
        select = self.select
        num = int(select.winfo_name()[-1])

        searchimg = f"!frame.!frame2.bot{num}.!labelframe.botimg{num}"
        searchname = f"!frame.!frame2.bot{num}.botname{num}"
        selectimg1 = self.nametowidget(searchimg)
        selectimg1data = selectimg1["image"]
        selectname1 = self.nametowidget(searchname)
        selectname1data = selectname1["text"]
        selectlen1 = self.framelist[num].get()
        print(f"self.count={self.count}")
        if whitch == "before":
            num2 = num - 1
            print(f"num2={num2}")
        else:
            num2 = num + 1
            print(f"num2={num2}")
        if 0 <= num2 < self.count:
            select.configure(relief="raised")
            searchimg2 = f"!frame.!frame2.bot{num2}.!labelframe.botimg{num2}"
            searchname2 = f"!frame.!frame2.bot{num2}.botname{num2}"
            selectimg2 = self.nametowidget(searchimg2)
            selectimg2data = selectimg2["image"]
            selectname2 = self.nametowidget(searchname2)
            selectname2data = selectname2["text"]
            selectlen2 = self.framelist[num2].get()

            selectimg1.configure(image=selectimg2data)
            selectimg2.configure(image=selectimg1data)
            selectname1.configure(text=selectname2data)
            selectname2.configure(text=selectname1data)
            self.framelist[num].set(selectlen2)
            self.framelist[num2].set(selectlen1)

            self.select = self.nametowidget(f"!frame.!frame2.bot{num2}")
            self.select.configure(relief="sunken")

            self.pathlist[num],self.pathlist[num2] = self.pathlist[num2],self.pathlist[num]
            self.piclist[num],self.piclist[num2] = self.piclist[num2],self.piclist[num]
            self.namelist[num],self.namelist[num2] = self.namelist[num2],self.namelist[num]
            self.framelist[num],self.framelist[num2] = self.framelist[num2],self.framelist[num]
        else:
            return "break"
        
    def rotateimage(self,lr):
        if lr == "left":
            lr = 1
        else:
            lr = -1
        num = int(self.select.winfo_name()[-1])
        searchimg = f"!frame.!frame2.bot{num}.!labelframe.botimg{num}"
        selectimg = self.piclist[num]
        rotateimg = selectimg.rotate(90 * lr)
        self.piclist[num] = rotateimg
        self.clear_topimage()
        self.getimage_top(num)
        size = self.scale_box(rotateimg,130)
        rotateimg = rotateimg.resize(size)
        rotateimg = ImageTk.PhotoImage(rotateimg)
        self.nametowidget(searchimg).configure(image=rotateimg)
        self.nametowidget(searchimg).image = rotateimg

    def mirrorimage(self):
        num = int(self.select.winfo_name()[-1])
        searchimg = f"!frame.!frame2.bot{num}.!labelframe.botimg{num}"
        selectimg = self.piclist[num]
        mirrorimg = ImageOps.mirror(selectimg)
        self.piclist[num] = mirrorimg
        self.clear_topimage()
        self.getimage_top(num)
        size = self.scale_box(mirrorimg,130)
        mirrorimg = mirrorimg.resize(size)
        mirrorimg = ImageTk.PhotoImage(mirrorimg)
        self.nametowidget(searchimg).configure(image=mirrorimg)
        self.nametowidget(searchimg).image = mirrorimg

    def copyimage(self):
        num = int(self.select.winfo_name()[-1])
        imgpath = self.pathlist[num]
        self.name = os.path.basename(imgpath)
        self.pathlist.append(imgpath)
        pic = self.piclist[num]
        size = self.piclist[0].size
        self.piclist.append(pic.resize(size))
        self.namelist.append(self.name)
        self.framelist.append(tk.IntVar(value=1))
        self.clear_topimage()
        self.select.configure(relief="raised")
        self.getimage_top(self.count)
        self.getimage_bot(self.count)
        self.count = self.count + 1
        self.selectnum = self.selectnum + 1

    def saveimage(self):
        if self.flag:
            savename = filedialog.asksaveasfilename(initialfile="新しいGIF画像", filetypes=[("GIF",".gif")], defaultextension=".gif")
            if savename == "":
                return "break"
            mms = 1000 / int(self.editfps.get())
            conv = []
            for slice in self.framelist:
                conv.append(int(slice.get() * mms))
            print(conv)
            self.piclist[0].save(savename, save_all=True, loop=0, append_images=self.piclist[1:], duration=conv)
        else:
            return print("ERROR")
        

if __name__ == "__main__":
    app = MyApp()
    app.title("GIFconverter")
    app.geometry("800x600")
    app.mainloop()
