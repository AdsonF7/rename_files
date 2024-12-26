"""
Module for manipulating the application's graphical interface

Author: Adson Felipe
Date: 2024-07-01
"""

import os
import glob
import pathlib
from tkinter import Tk, Text, Button, Entry, Label, StringVar, END, DISABLED, NORMAL, Frame, NSEW
from mutagen.easyid3 import EasyID3


class GUI(Tk):

  def __init__(self):
    """
      Application graphical interface class
    """
    super().__init__()
    self.sv_folder = StringVar(self)
    self.sv_extension = StringVar(self)
    self.sv_extension.set("mp3")
    self.frame1 = Frame(self)
    self.frame2 = Frame(self)
    self.frame3 = Frame(self)
    lb_folder = Label(self.frame1, text="Folder")
    lb_folder.grid(column=0, row=0)
    lb_extension = Label(self.frame1, text="Extension")
    lb_extension.grid(column=0, row=1)
    self.et_folder = Entry(self.frame1, textvariable=self.sv_folder)
    self.et_folder.grid(column=1, row=0)
    self.et_extension = Entry(self.frame1, textvariable=self.sv_extension)
    self.et_extension.grid(column=1, row=1)
    self.bt_fill = Button(self.frame1, text="Fill")
    self.bt_fill.grid(column=0, row=2)
    self.tx_source = Text(self.frame2, state=DISABLED)
    self.tx_source.grid(column=0, row=0)
    self.tx_source_tracknumber = Text(self.frame2, state=DISABLED, width=2)
    self.tx_source_tracknumber.grid(column=1, row=0)
    self.tx_target = Text(self.frame2, state=DISABLED)
    self.tx_target.grid(column=2, row=0)
    self.tx_target_tracknumber = Text(self.frame2, state=DISABLED, width=2)
    self.tx_target_tracknumber.grid(column=3, row=0)
    lb_tracknumber = Label(self.frame3, text="Track Number")
    lb_tracknumber.grid(column=0, row=0)
    self.et_tracknumber = Entry(self.frame3)
    self.et_tracknumber.grid(column=1, row=0)
    lb_filename = Label(self.frame3, text="Filename")
    lb_filename.grid(column=0, row=1)
    self.et_filename = Entry(self.frame3)
    self.et_filename.grid(column=1, row=1)
    self.bt_save = Button(self.frame3, text="Save")
    self.bt_save.grid(column=0, row=2)
    self.frame1.grid(column=0, row=0, sticky=NSEW)
    self.frame2.grid(column=0, row=1, sticky=NSEW)
    self.frame3.grid(column=0, row=2, sticky=NSEW)
    
    self.metadatas = []
    self.txs = [self.tx_source, self.tx_target, self.tx_source_tracknumber, self.tx_target_tracknumber]
    self.bt_fill.bind("<ButtonRelease-1>", lambda x: self.fill())
    self.bt_save.bind("<ButtonRelease-1>", lambda x: self.save())
    self.mainloop()

  def split(string, pos):
    result = []
    for filepath in self.filespaths:
      result.append(filepath.stem.split(string)[pos])
    return result

  def pos(start, end):
    result = []
    for filepath in self.filespaths:
      result.append(filepath.stem[start, end])
    return result
  
  #split(pos(0,1),"-",0)
  def fill(self):
    self.clear()
    folder = self.sv_folder.get()
    #if folder.count("\\\\") == 0:
    #  self.sv_folder.set(folder.replace("\\", "\\\\"))
    self.all_to_enabled()
    i = 1
    for file in glob.glob(f"{self.sv_folder.get()}\\*.{self.sv_extension.get()}"):
      path = pathlib.PurePath(file)
      old_tracknumber = self.get_tracknumber(file)
      new_tracknumber = path.stem[:2]
      new_filename = "artist-" + path.stem[5:].lower().replace(" ", "_")
      
      self.tx_source.insert(END, path.stem)
      self.tx_source.insert(END, "\n")
      self.tx_target.insert(END, new_filename)
      self.tx_target.insert(END, "\n")
      self.metadatas.append({"path": path, "tracknumber": new_tracknumber, "name": new_filename })
      self.tx_source_tracknumber.insert(END, old_tracknumber)
      self.tx_target_tracknumber.insert(END, new_tracknumber)
      self.tx_source_tracknumber.insert(END, "\n")
      self.tx_target_tracknumber.insert(END, "\n")
      i += 1
    self.all_to_disabled()
    
    #self.sv_folder.get())

  def save(self):
    for i in self.metadatas:
      self.set_tracknumber(i["path"], i["tracknumber"])
      self.rename(i["path"], i["name"])
    
  def rename(self, old_path, new_name):
    os.rename(old_path, pathlib.PurePath(old_path.parent, new_name + old_path.suffix))
    
  def get_tracknumber(self, file):
    audio = EasyID3(file)
    tracknumber = audio.get("tracknumber")
    if not tracknumber:
      tracknumber = ""
    return tracknumber

  def set_tracknumber(self, file, tracknumber):
    audio = EasyID3(file)
    audio["tracknumber"] = tracknumber
    audio.save()
    
  def all_to_enabled(self):
    for i in self.txs:
      i["state"] = NORMAL

  def all_to_disabled(self):
    for i in self.txs:
      i["state"] = DISABLED
      
  def clear(self):
    for i in self.txs:
      i["state"] = NORMAL
      i.delete("1.0", END)
      i["state"] = DISABLED
