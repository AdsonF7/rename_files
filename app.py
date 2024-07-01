import pathlib
import os
from mutagen.easyid3 import EasyID3
 
class App:
  
  def __init__(self):
    pass
    
  def rename_file(self, old_path, new_name):
    """
      method used to rename file

      Args:
        old_path (WindowPath): 
        new_name (str): New file name

      Returns:
        boolean: if there is no error, it returns true
    """
    os.rename(old_path, pathlib.PurePath(old_path.parent, new_name + old_path.suffix))

  def set_tracknumber(self, pathfile, tracknumber):
    """
      method to change tracknumber

      Args:
        pathfile (WindowsPath): 
        tracknumber (int): new tracknumber audio file
        
      Returns:
        boolean: if there is no error, it returns true
    """
    audio = EasyID3(pathfile)
    audio["tracknumber"] = tracknumber
    audio.save()
