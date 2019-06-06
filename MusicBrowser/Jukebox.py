import sqlite3
try:
    import tkinter
except ImportError:   # python 2
    import Tkinter as tkinter

# conn = sqlite3.connect('music.sqlite')


class ScrollBox(tkinter.Listbox):

    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)

        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

    def grid(self, row, column, sticky='nsw', rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self.scrollbar.grid(row=row, column=column, stick='nse', rowspan=rowspan)
        self['yscrollcommand'] = self.scrollbar.set


class DataListBox(ScrollBox):

    def __init__(self, window, connection, table, field, sort_order=(), **kwargs):
        super().__init__(window, **kwargs)

        self.linked_box = None
        self.link_field = None
        self.link_value = None
        self.cursor = connection.cursor()
        self.table = table
        self.field = field

        self.bind('<<ListboxSelect>>', self.on_select)

        self.sql_select = "SELECT " + self.field + ", _id" + " FROM " + self.table

        if sort_order:
            self.sql_sort = " ORDER BY " + ','.join(sort_order)
        else:
            self.sql_sort = " ORDER BY " + self.field

    def clear(self):
        self.delete(0, tkinter.END)

    def link(self, widget, link_field):
        self.linked_box = widget
        widget.link_field = link_field

    def requery(self, link_value=None):
        self.link_value = link_value # store the id so we know the 'master ' record we're populated from
        if link_value and self.link_field:
            sql = self.sql_select + " WHERE " + self.link_field + "=?" + self.sql_sort
            print(sql)   # TODO delete this line
            self.cursor.execute(sql, (link_value, ))
        else:
            print(self.sql_select + self.sql_sort)  # TODO delete this line
            self.cursor.execute(self.sql_select + self.sql_sort)

        # clear the listbox contents bef re-loading
        self.clear()
        for value in self.cursor:
            self.insert(tkinter.END, value[0])

        if self.linked_box:
            self.linked_box.clear()

    def on_select(self, event):
        if self.linked_box:
            print(self is event.widget)  # TODO delete this line
            index = self.curselection()[0]
            value = self.get(index),

            # get the id from the db row
            # make sure we're getting the correct one by including the link_value if appropriate
            if self.link_value:
                value = value[0], self.link_value
                sql_where = " WHERE " + self.field + "=? AND " + self.link_field + "=?"
            else:
                sql_where = " WHERE " + self.field + "=?"
            # get the artist ID from the database row
            link_id = self.cursor.execute(self.sql_select + sql_where, value).fetchone()[1]

            # SELECT name, _id, FROM albums WHERE name='Greatest hits'
            self.linked_box.requery(link_id)

        # artist_id = conm.execute("SELECT artists._id FROM artists WHERE artists.name = ?", artist_name).fetchone()
        # alist = []
        # for row in conm.execute("SELECT albums.name FROM albums WHERE albums.artist = ?
        # ORDER BY albums.name", artist_id):
        #     alist.append(row[0])
        # albumLV.set(tuple(alist))
        # songLV.set(("Choose an album",))

# def get_songs(event):
#     lb = event.widget
#     index = int(lb.curselection()[0])
#     album_name = lb.get(index),
#
#     # get the artist id from the db row
#     album_id = conn.execute("SELECT albums._id FROM albums WHERE albums.name = ?", album_name).fetchone()
#     alist = []
#     for x in conn.execute("SELECT songs.title FROM songs WHERE songs.album=? ORDER BY songs.track", album_id):
#         alist.append(x[0])
#     songLV.set(tuple(alist))


if __name__ == '__main__':
    conn = sqlite3.connect('music.sqlite')
    mainWindow = tkinter.Tk()
    mainWindow.title("Music DB Browser")
    mainWindow.geometry('1024x768')

    # column conf
    mainWindow.columnconfigure(0, weight=2)
    mainWindow.columnconfigure(1, weight=2)
    mainWindow.columnconfigure(2, weight=2)
    mainWindow.columnconfigure(3, weight=1)  # spacer column on the right

    # row config

    mainWindow.rowconfigure(0, weight=1)
    mainWindow.rowconfigure(1, weight=5)
    mainWindow.rowconfigure(2, weight=5)
    mainWindow.rowconfigure(3, weight=1)

    # ==== Labels =====

    tkinter.Label(mainWindow, text="Artists").grid(row=0, column=0)
    tkinter.Label(mainWindow, text="Albums").grid(row=0, column=1)
    tkinter.Label(mainWindow, text="Songs").grid(row=0, column=2)

    # ==== Artists ListBox =====

    artistList = DataListBox(mainWindow, conn, "artists", "name")
    artistList.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
    artistList.config(border=2, relief='sunken')

    artistList.requery()
    # for artist in conm.execute("SELECT artists.name FROM artists ORDER BY artists.name"):
    #     artistList.insert(tkinter.END, artist[0])

    # artistScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL,
    # command=artistList.yview) ##Implemented in class
    # artistScroll.grid(row=1, column=0, sticky='nse', rowspan=2)
    # artistList['yscrollcommand'] = artistScroll.set

    # ==== Albums ListBox =====

    albumLV = tkinter.Variable(mainWindow)
    albumLV.set(("Choose an artists",))
    albumList = DataListBox(mainWindow, conn, "albums", "name", sort_order=("name",))
    # albumList.requery()
    albumList.grid(row=1, column=1, sticky='nsew', padx=(30, 0))
    albumList.config(border=2, relief='sunken')

    # albumList.bind('<<ListboxSelect>>', get_songs)
    artistList.link(albumList, "artist")

    # albumScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL,
    # command=albumList.yview)  ## Implemented in class
    # albumScroll.grid(row=1, column=1, sticky='nse', rowspan=2)
    # albumList['yscrollcommand'] = albumScroll.set

    # ==== Songs ListBox =====

    songLV = tkinter.Variable(mainWindow)
    songLV.set(("Choose an album ", ))
    songList = DataListBox(mainWindow, conn, "songs", "title", sort_order=("track", "title"))
    # songList.requery()
    songList.grid(row=1, column=2, sticky='nsew', padx=(30, 0))
    songList.config(border=2, relief='sunken')

    albumList.link(songList, "album")

    # ==== Main loop ======
    # testList = range(0, 100)
    # albumLV.set(tuple(testList))
    mainWindow.mainloop()
    print("Closing db connection")
    conn.close()
