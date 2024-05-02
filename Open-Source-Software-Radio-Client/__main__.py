import vlc
import time
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import requests
from modules.Gradian import GradientFrame
from modules.Constants import Constants
from urllib.request import urlopen
import json
os.add_dll_directory(os.getcwd())


class Music:
    def __init__(self, id, name, image_path, artists):
        self.id = id
        self.name = name
        self.image_path = image_path
        self.artists = artists

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['fg']
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.insert_placeholder()

    def insert_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def on_focus_in(self, event):
        if self['fg'] == self.placeholder_color:
            self.delete(0, "end")
            self['fg'] = self.default_fg_color

    def on_focus_out(self, event):
        if not self.get():
            self.insert_placeholder()
music_name_to_index = {}
class GUI(tk.Frame):
    file_image_selected = None
    file_mp3_selected = None
    input_name_music = ""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(background='#192533')
        self.master.title("Radio app")
        self.master.geometry("1000x600")
       
        

        # event Play mp3

        def handle_play_mp3(path):
            url = "http://localhost:5000/play-music/" + str(path)
            media_player = Constants.media_player
            media = vlc.Media(url)
            media_player.set_media(media)
            media_player.play()
            duration = media_player.get_length() / 1000
            while (duration > 0):
                duration = duration - 1

        # event Previous music
        def handle_prev():
            if (Constants.index_select > 0 and Constants.index_select < len(Constants.list_music)):
                self.seekbar['value'] = 0
                self.listbox.select_clear(Constants.index_select)
                Constants.index_select = Constants.index_select - 1
                Constants.music_selected = Constants.list_music[Constants.index_select]
                handle_play_mp3(Constants.music_selected['path'])
                self.listbox.select_set(Constants.index_select)
                if (Constants.music_selected['image'] == ""):
                    img = ImageTk.PhotoImage(Image.open(
                        r"output.png"))
                    self.lbImage.configure(image=img)
                    self.lbImage.image = img
                else:
                    URL = "http://127.0.0.1:5000/photo/" + \
                        str(Constants.music_selected['image'])
                    u = urlopen(URL)
                    raw_data = u.read()
                    u.close()
                    img = ImageTk.PhotoImage(data=raw_data)
                self.lbImage.configure(image=img)
                self.lbImage.image = img
                self.lb_artist.configure(text=f"Singer: {Constants.music_selected['artists']}")
                self.lb_music_name.configure(text=Constants.music_selected['name'])
                self.lb_music_name.pack(padx=20, pady=(20, 0), side="top")
            else:
                Constants.index_select = len(Constants.list_music) - 1
                self.seekbar['value'] = 0
                self.listbox.select_clear(Constants.index_select)
                Constants.music_selected = Constants.list_music[Constants.index_select]
                handle_play_mp3(Constants.music_selected['path'])
                self.listbox.select_set(Constants.index_select)
                if (Constants.music_selected['image'] == ""):
                    img = ImageTk.PhotoImage(Image.open(
                        r"output.png"))
                    self.lbImage.configure(image=img)
                    self.lbImage.image = img
                else:
                    URL = "http://127.0.0.1:5000/photo/" + \
                        str(Constants.music_selected['image'])
                    u = urlopen(URL)
                    raw_data = u.read()
                    u.close()
                    img = ImageTk.PhotoImage(data=raw_data)
                self.lbImage.configure(image=img)
                self.lbImage.image = img
                self.lb_artist.configure(text=f"Singer: {Constants.music_selected['artists']}")
                self.lb_music_name.configure(text=Constants.music_selected['name'])
                self.lb_music_name.pack(padx=20, pady=(20, 0), side="top")
            


        # event Pause/continue music
        def handle_paused():
            if (Constants.index_select >= 0 and Constants.index_select < len(Constants.list_music)):
                media_player = Constants.media_player
                # No play
                if (Constants.isPlay == False):
                    imgPrev = ImageTk.PhotoImage(Image.open(
                        r"assets\\pause.png"))
                    media_player.play()
                    Constants.isPlay = True
                # Playing
                else:
                    imgPrev = ImageTk.PhotoImage(Image.open(
                        r"assets\\play.png"))
                    media_player.pause()
                    Constants.isPlay = False
                self.btnPaused.configure(image=imgPrev)
                self.btnPaused.image = imgPrev

        # event next music
        def handle_next():
            if (Constants.index_select < len(Constants.list_music) - 1 and Constants.index_select > -1):
                self.seekbar['value'] = 0
                self.listbox.select_clear(Constants.index_select)
                Constants.index_select = Constants.index_select + 1
                Constants.music_selected = Constants.list_music[Constants.index_select]
                handle_play_mp3(Constants.music_selected['path'])
                self.listbox.select_set(Constants.index_select)
                if (Constants.music_selected['image'] == ""):
                    img = ImageTk.PhotoImage(Image.open(
                        r"output.png"))
                    self.lbImage.configure(image=img)
                    self.lbImage.image = img
                else:
                    URL = "http://127.0.0.1:5000/photo/" + \
                        str(Constants.music_selected['image'])
                    u = urlopen(URL)
                    raw_data = u.read()
                    u.close()
                    img = ImageTk.PhotoImage(data=raw_data)
                self.lbImage.configure(image=img)
                self.lbImage.image = img
                self.lb_artist.configure(text=f"Singer: {Constants.music_selected['artists']}")
                self.lb_music_name.configure(text=Constants.music_selected['name'])
                self.lb_music_name.pack(padx=20, pady=(20, 0), side="top")
            elif (Constants.index_select == len(Constants.list_music) - 1):
                self.seekbar['value'] = 0
                self.listbox.select_clear(Constants.index_select)
                Constants.index_select = 0
                Constants.music_selected = Constants.list_music[Constants.index_select]
                handle_play_mp3(Constants.music_selected['path'])
                self.listbox.select_set(Constants.index_select)
                if (Constants.music_selected['image'] == ""):
                    img = ImageTk.PhotoImage(Image.open(
                        r"output.png"))
                    self.lbImage.configure(image=img)
                    self.lbImage.image = img
                else:
                    URL = "http://127.0.0.1:5000/photo/" + \
                        str(Constants.music_selected['image'])
                    u = urlopen(URL)
                    raw_data = u.read()
                    u.close()
                    img = ImageTk.PhotoImage(data=raw_data)
                self.lbImage.configure(image=img)
                self.lbImage.image = img
                self.lb_artist.configure(text=f"Singer: {Constants.music_selected['artists']}")
                self.lb_music_name.configure(text=Constants.music_selected['name'])
                self.lb_music_name.pack(padx=20, pady=(20, 0), side="top")

        def handle_search(event=None):
    # Lấy truy vấn tìm kiếm nhập bởi người dùng
           search_term = self.search_entry.get().lower()

    # Xóa danh sách trước khi điền vào kết quả tìm kiếm
           self.listbox.delete(0, 'end')
           self.listbox_artists.delete(0, 'end')
           music_name_to_index.clear() #Xóa dữ liệu cũ
           seen_artists = set()  # Tạo một set để lưu trữ các nghệ sĩ đã xuất hiện

    # Lặp qua danh sách bài hát
           for index, music in enumerate(Constants.list_music):
        # So sánh tên bài hát với truy vấn tìm kiếm
             if search_term in music['name'].lower() or search_term in music['artists'].lower():
            # Nếu truy vấn tìm kiếm phù hợp với tên bài hát, thêm vào listbox
               self.listbox.insert('end', music['name'])
               music_name_to_index[music['name']] = index
               artists = music['artists']
               # Lặp qua danh sách nghệ sĩ của bài hát và thêm vào listbox_artists nếu chưa xuất hiện trước đó
               for artist in artists.split(', '):
                   if artist not in seen_artists:
                      self.listbox_artists.insert('end', artist)
                      seen_artists.add(artist)

# Gắn hàm tìm kiếm vào sự kiện kích hoạt khi người dùng nhập truy vấn tìm kiếm
        # self.search_entry.bind('<KeyRelease>', handle_search)
        # def handle_search_artist(event=None):
        #  # Lấy truy vấn tìm kiếm nhập bởi người dùng
        #   search_term = self.search_entry.get().lower()

        #  # Xóa danh sách trước khi điền vào kết quả tìm kiếm
        #   self.listbox.delete(0, 'end')
        #   music_name_to_index.clear() # Xóa dữ liệu cũ

        #  # Lặp qua danh sách nghệ sĩ
        #   for index, artist in enumerate(Constants.list_music):
        #     # So sánh tên nghệ sĩ với truy vấn tìm kiếm
        #     if search_term in artist['artists'].lower():
        #     # Nếu truy vấn tìm kiếm phù hợp với tên nghệ sĩ, thêm vào listbox
        #       self.listbox_artists.select_clear(0, 'end')  # Xóa bỏ việc chọn trước đó
        #       self.listbox_artists.select_set(index)  # Chọn nghệ sĩ tương ứng
        #       self.listbox.insert('end', artist['name'])  # Thêm tên bài hát vào listbox
        #       music_name_to_index[artist['name']] = index  # Lưu chỉ mục tương ứng

        # event Play mp3
        def onselect(evt):
            self.seekbar['value'] = 0
            imgPrev = ImageTk.PhotoImage(Image.open(
                r"assets\\pause.png"))
            self.btnPaused.configure(image=imgPrev)
            self.btnPaused.image = imgPrev
            if not self.listbox.curselection():
                return
            # Lấy index của dòng được chọn
            index = self.listbox.curselection()[0]
            # Lấy tên bài hát từ listbox
            music_name = self.listbox.get(index)
            if music_name in music_name_to_index:
            # Sử dụng tên bài hát để lấy index ban đầu trong danh sách tổng thể
              original_index = music_name_to_index[music_name]
            # Lấy tên nghệ sĩ từ danh sách tổng thể 
              artist_name = Constants.list_music[original_index]['artists']
            # Lấy chỉ mục của nghệ sĩ trong danh sách nghệ sĩ
              artist_index = [i for i, artist in enumerate(self.listbox_artists.get(0, 'end')) if artist == artist_name]
              if artist_index:
                  # Chọn nghệ sĩ tương ứng trong danh sách nghệ sĩ
                  self.listbox_artists.select_clear(0, 'end')
                  self.listbox_artists.select_set(artist_index[0])
              selected_music = Constants.list_music[original_index]
            else:
        # Nếu không tìm thấy bài hát trong từ điển, lấy thông tin từ danh sách trực tiếp
              selected_music = Constants.list_music[index]
              artist_name = selected_music['artists']
              artist_index = [i for i, artist in enumerate(self.listbox_artists.get(0, 'end')) if artist == artist_name]
              if artist_index:
                  # Chọn nghệ sĩ tương ứng trong danh sách nghệ sĩ
                  self.listbox_artists.select_clear(0, 'end')
                  self.listbox_artists.select_set(artist_index[0])
    
    
            (id, image, name,
             path) = selected_music['id'], selected_music['image'], selected_music['name'], selected_music['path']
            Constants.index_select = index
            Constants.music_selected = selected_music
            self.lb_artist.configure(text=f"Singer: {selected_music['artists']}")
            self.lb_music_name.configure(text=name)
            self.lb_music_name.pack(padx=20, pady=(10, 0), side="top")
            if (Constants.solve != None):
                self.seekbar1.after_cancel(Constants.solve)
            if (image == ""):
                img = ImageTk.PhotoImage(Image.open(
                    r"output.png"))
                self.lbImage.configure(image=img)
                self.lbImage.image = img
            else:
                URL = "http://127.0.0.1:5000/photo/" + str(image)
                u = urlopen(URL)
                raw_data = u.read()
                u.close()
                img = ImageTk.PhotoImage(data=raw_data)
                self.lbImage.configure(image=img)
                self.lbImage.image = img
            handle_play_mp3(str(path))
            play_time()

        def upload_image():
            # [("pnj file", "*.pnj"), ("jpg file", "*.jpg")]
            f_types = [('Jpg Files', ['*.jpg','*.png'])]
            self.file_image_selected = filedialog.askopenfilename(
                initialdir=r'C:\\Downloads', filetypes=f_types)
            imageFileBaseName = os.path.basename(self.file_image_selected)
            self.image_entry.delete(0, 'end')  # clear any existing text
            # insert selected file path
            self.image_entry.insert(0, imageFileBaseName)

        # event choose file mp3
        def upload_mp3():
            f_types = [("Audio Files", ".wav .ogg"),   ("All Files", "*.*")]
            self.file_mp3_selected = filedialog.askopenfilename(
                initialdir=r'C:\\Downloads')
            # dir = filedialog.askopenfilename(
            #     initialdir="/", title="chon file", filetypes=(("mp3 file", "*.mp3"), ("all file", "*.*")))
            mp3FileBaseName = os.path.basename(self.file_mp3_selected)
            fileNameExtention = mp3FileBaseName.split('.')
            fileNameExtention = "." + fileNameExtention[len(fileNameExtention) - 1]
            arr = [".mp3",".aac",".wma",".wav",".flac",".ogg",".aiff",".alac",".m4a"]
            if mp3FileBaseName != None and fileNameExtention in arr:
                self.mp3file_entry.delete(0, 'end')
                self.mp3file_entry.insert(0, mp3FileBaseName)
            else:
                self.file_mp3_selected = None
                tk.messagebox.showerror(
                    "Error", "Please choose the correct format !!!")

        def upload_data_to_server():
            url = "http://127.0.0.1:5000/uploads"
            files = {}
            if self.file_mp3_selected and self.name_entry.get() and self.artist_entry.get():
                payload = {'name': self.name_entry.get().strip(),'artists': self.artist_entry.get().strip()}
                files = {
                    'data': (None, json.dumps(payload), 'application/json'),
                    'file': open(self.file_mp3_selected, 'rb'),
                }
                if self.file_image_selected:
                    files['image'] = open(self.file_image_selected, 'rb')
                # headers = {'Content-Type': 'multipart/form-data'}
                res = requests.post(url, files=files)
                if (res.status_code == 200):
                    Constants.list_music.insert(
                        len(Constants.list_music), res.json())
                    self.listbox.insert(END, res.json()['name'])
                    self.listbox_artists.insert(END, res.json()['artists'])
                    self.add_song_win.destroy()
                    self.file_image_selected = None
                    self.file_mp3_selected = None
                else:
                    tk.messagebox.showerror(
                        "Error", "Oh No ! What Wrong From Server !!!")
            else:
                tk.messagebox.showerror(
                    "Error", "Please enter fill input NAME and FILE MUSIC !!!")

        # event upload mp3
        def handle_add_music():
            self.add_song_win = tk.Toplevel()
            # self.add_song_win.attributes('-topmost', True)
            self.add_song_win.geometry("300x150")
            self.add_song_win.title("Add Music")
            lb_name = tk.Label(self.add_song_win, text="Song Name")
            self.name_entry = tk.Entry(self.add_song_win)

            lb_mp3file = tk.Label(self.add_song_win, text="File mp3")
            self.mp3file_entry = tk.Entry(self.add_song_win)

            bt_select_file = tk.Button(
            self.add_song_win, text="Select", command=upload_mp3)
            self.mp3file_entry.delete(0)
            self.mp3file_entry.insert(0, "Please choose file mp3 !!!")

            lb_image = tk.Label(self.add_song_win, text="Image")
            self.image_entry = tk.Entry(self.add_song_win)

            bt_select_image = tk.Button(
                self.add_song_win, text="Select", command=upload_image)
            self.image_entry.delete(0)
            self.image_entry.insert(0, "Please choose file image !!!")
            lb_artist = tk.Label(self.add_song_win, text="Artist")
            self.artist_entry = tk.Entry(self.add_song_win)
            btn_them = tk.Button(self.add_song_win, text="Upload",
                                 command=upload_data_to_server)
            btn_huy = tk.Button(self.add_song_win, text="Cancel",
                                command=self.add_song_win.destroy)

            lb_name.grid(row=0, column=0)
            self.name_entry.grid(row=0, column=1)

            lb_mp3file.grid(row=1, column=0)
            self.mp3file_entry.grid(row=1, column=1)
            bt_select_file.grid(row=1, column=2)

            lb_image.grid(row=2, column=0)
            self.image_entry.grid(row=2, column=1)
            bt_select_image.grid(row=2, column=2)
            lb_artist.grid(row=3, column=0)
            self.artist_entry.grid(row=3, column=1)

            btn_huy.grid(row=4, column=1, pady=20)
            btn_them.grid(row=4, column=2)
            
        # event scroll seekbar when play mp3
        def play_time():
            media_player = Constants.media_player
            if (media_player.is_playing() == 1):
                Constants.isPlay = True
                current_time = int(media_player.get_length() / 1000)
                current_length = float(media_player.get_length() / 1000)
                convert_current_time = time.strftime(
                    '%H:%M:%S', time.gmtime(float(media_player.get_time() / 1000)))
                convert_current_length = time.strftime(
                    '%H:%M:%S', time.gmtime(current_length))
                self.seekbar1.config(
                    text=str(convert_current_time) + "/" + str(convert_current_length))

                self.seekbar['value'] += float(100/current_time)
            Constants.solve = self.seekbar1.after(1000, play_time)

        # event click seekbar
        def on_seekbar_click(event):
            self.seekbar['value'] = event.x / 3
            # get position on seekbar tool
            position = self.seekbar.get()
            media_player = Constants.media_player
            time = ((media_player.get_length() / 1000) / 100) * position
            media_player.set_time(int(time * 1000))

        # Frame left (Play mp3)
        self.frameL = GradientFrame(self.master, width=500,
                                    height=600, borderwidth=1, relief="sunken")
        self.frameL.pack(side="left", fill="y")



        # Frame Right (List mp3)
        self.frameR = GradientFrame(self.master, width=300,
                                    height=600,
                                    borderwidth=1, relief="sunken")
        self.frameR.pack(side="right", fill="both", expand=True)

        # Tạo thanh tìm kiếm
        self.search_entry = PlaceholderEntry(self.frameR, placeholder="Tìm kiếm bài hát")
        self.search_entry.pack(side="top", padx=10, pady=10, fill="x")
        self.search_entry.bind('<KeyRelease>', handle_search)

        self.lb_artist = tk.Label(self.frameL, text="",bg='#192533', fg="white", font=("Arial", 12))
        self.lb_artist.place(x=120,y=20)

        # Label image music (Left)
        img = ImageTk.PhotoImage(Image.open(
            r"output.png"))
        self.lbImage = tk.Label(self.frameL, image=img,
                           width=300, height=300, bg='#192533')
        self.lbImage.image = img
        self.lbImage.pack(padx=50, pady=50, side="top")

        # Label name music (Left)
        self.lb_music_name = tk.Label(self.frameL, text="", bg='#192533', fg="white", font=("Arial", 12))  # Sử dụng font-size 12
        # self.lb_music_name.pack(padx=20, pady=(20, 0), side="top")
        # Label show time music (Left)
        self.seekbar1 = tk.Label(self.frameL, text='', relief=GROOVE, anchor=E)
        self.seekbar1.pack(fill=X, side=BOTTOM, ipady=2)

        def slide(x):
            pass

        # Seekbar (Left)
        self.seekbar = ttk.Scale(
            self.frameL, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=300)
        self.seekbar.pack()
        self.seekbar.bind('<Button-1>', on_seekbar_click)

        # btn previous, pause, next... (Left)
        imgPrev = ImageTk.PhotoImage(Image.open(
            r"assets\\back.png"))
        btnPrev = tk.Button(self.frameL, image=imgPrev,
                            width=35, height=35, border=0, command=handle_prev)
        btnPrev.image = imgPrev
        btnPrev.place(x=90, y=480, width=35, height=35)

        imgPaused = ImageTk.PhotoImage(Image.open(
            r"assets\\play.png"))
        self.btnPaused = tk.Button(
            self.frameL, image=imgPaused, width=35, height=35, command=handle_paused)
        self.btnPaused.image = imgPaused
        self.btnPaused.place(x=185, y=480, width=35, height=35)

        imgNext = ImageTk.PhotoImage(Image.open(
            r"assets\\next.png"))
        btnNext = tk.Button(self.frameL, image=imgNext,
                            width=35, height=35, command=handle_next)
        btnNext.image = imgNext
        btnNext.place(x=280, y=480, width=35, height=35)

        


        # List music (Right)
        self.listbox_label = tk.Label(self.frameR, text="List of Music", bg='#192533', fg="white", font=("Arial", 12))
        self.listbox_label.pack(side="top", padx=40, pady=(10, 0))
        self.listbox_label.place(x=90,y=40)
        self.listbox = tk.Listbox(self.frameR, width=50, height=25)
        self.listbox.pack(side="top", padx=40, pady=(0, 50), expand=True)
        self.listbox.place(x=10,y=60)
        try:
           res = requests.get(
            "http://127.0.0.1:5000/get-all-music")
           res.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code.
           if res.text.strip():  # Making sure the response is not empty
              Constants.list_music = res.json()
              for music in Constants.list_music:
                  self.listbox.insert(END, music['name'])
              self.listbox.bind('<<ListboxSelect>>', onselect)
           else:
              Constants.list_music = []
              print("Server returned an empty response.")
              tk.messagebox.showerror("Error", "Server returned an empty response.")
        except requests.exceptions.HTTPError as http_err:
           print(f"HTTP error occurred: {http_err}")
           tk.messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as e:
           print(f"An error occurred: {e}")
           tk.messagebox.showerror("Error", f"An error occurred: {e}")
        except json.decoder.JSONDecodeError:
           print("Response content is not valid JSON.")
           tk.messagebox.showerror("Error", "Response content is not valid JSON.")

        #List Artists
        self.listbox_artists_label = tk.Label(self.frameR, text="List of Artists", bg='#192533', fg="white", font=("Arial", 12))
        self.listbox_artists_label.pack(side="top", padx=40, pady=(10, 0))
        self.listbox_artists_label.place(x=440,y=40)
        self.listbox_artists = tk.Listbox(self.frameR, width=50, height=25)
        self.listbox_artists.pack(side="right", padx=40, pady=(0, 50), expand=True)
        self.listbox_artists.place(x=360,y=60)
        
        # res = requests.get(
        #     "http://127.0.0.1:5000/get-all-music"
        # )
        # artists = res.json()
        # for artist in artists:
        #     self.listbox_artists.insert(END, artist['artists'])
        # self.listbox.bind('<<ListboxSelect>>', onselect)
        try:
           res_artists = requests.get("http://127.0.0.1:5000/get-all-music")
           res_artists.raise_for_status()
           if res_artists.text.strip():  # Kiểm tra response không rỗng
              data_artists = res_artists.json()
              seen_artists = set()
              for item in data_artists:
            # Mỗi item sẽ có thể chứa nhiều artists, chia cắt bởi dấu ","
                  artists = item.get('artists', '').split(', ')
                  for artist in artists:
                      if artist not in seen_artists:
                         self.listbox_artists.insert('end', artist)
                         seen_artists.add(artist)
                         self.listbox.bind('<<ListboxSelect>>', onselect)
           else:
                print("Server returned an empty response for artists.")
                tk.messagebox.showerror("Error", "Server returned an empty response for artists.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            tk.messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
        except json.decoder.JSONDecodeError:
            print("Response content is not valid JSON for artists.")
            tk.messagebox.showerror("Error", "Response content is not valid JSON for artists.")

        button_frame = tk.Frame(self.frameR)  # Tạo một frame con để chứa hai nút
        button_frame.pack(side="top", pady=(0, 10))  # Đặt frame con ở phía trên cùng của frameR
        button_frame.place(x=80,y=420)

        self.btnAdd = tk.Button(button_frame, text="Add Music", width=10, height=2, command=handle_add_music)
        self.btnAdd.pack(side="left", padx=(0, 10))  # Đặt nút "Add" bên trái

        self.btnDelete = tk.Button(button_frame, text="Delete Music", width=10, height=2, command=self.handle_delete_music)
        self.btnDelete.pack(side="left")  # Đặt nút "Delete" bên phải
    def update_artist(self):
            self.listbox_artists.delete(0, 'end')
            seen_artists = set()
            for music in Constants.list_music:
                for artist in music['artists'].split(', '):
                    if artist not in seen_artists:
                       self.listbox_artists.insert('end', artist)
                       seen_artists.add(artist)
        # event delete mp3
    def handle_delete_music(self):
            if Constants.index_select is not None and Constants.index_select >= 0:
               selected_music = Constants.list_music[Constants.index_select]
               music_id = selected_music['id']
               try:   
                 response = requests.get(f"http://127.0.0.1:5000/delete-music/{music_id}")
                 if response.status_code == 200 and response.json().get('message') == 'Delete Success':
                   self.listbox.delete(Constants.index_select)
                   Constants.list_music.pop(Constants.index_select)
                   self.update_artist()
                   Constants.index_select = None
                   Constants.isPlay = False
                   Constants.music_selected = {}
                   Constants.media_player.stop()
                   img = ImageTk.PhotoImage(Image.open(
                    r"output.png"))
                   self.lbImage.configure(image=img)
                   self.lbImage.image = img
                   self.lb_music_name.pack_forget()
                   imgPause = ImageTk.PhotoImage(Image.open(
                    r"assets\\play.png"))
                   self.btnPaused.configure(image=imgPause)
                   self.btnPaused.image = imgPause
                   tk.messagebox.showinfo('Success', 'Song deleted successfully.')
                 else:
                   tk.messagebox.showerror("Error", "Could not delete the song.")
               except requests.exceptions.RequestException as e:
                   tk.messagebox.showerror("Error", f"An error occurred: {e}")
            else:
                tk.messagebox.showinfo("Info", "Please select a song to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    # root.wm_attributes('-topmost', True)
    # root.wm_attributes('-transparentcolor', '#192533')
    gui.mainloop()
