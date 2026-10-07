
import subprocess
from pathlib import Path
import psutil
import sqlite3 as sql
from datetime import datetime
conn=sql.connect("mydatabase.db")
cur=conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS file_info(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 path TEXT NOT NULL,
                 name TEXT NOT NULL, 
                 is_marked INTEGER NOT NULL, 
                 last_seen TEXT )""")
conn.commit()
def file_prober():
        dis=True
        subf=True   
        while dis:
          disks = [part.device for part in psutil.disk_partitions()]
          drv_sel="\n".join(disks)
          disk_ui=subprocess.run(["fzf"],
                    input=drv_sel,
                    text=True,
                    capture_output=True)
          drive_selection=disk_ui.stdout.strip()
          if disk_ui.returncode==0:
            print("Drive selected successfully!")
          else:
            print(f"We approach ab error contact the developer for more details : {disk_ui.stderr}")
          current_folder=Path(drive_selection)

           
          print(current_folder.exists())

          while subf:
            subfolders_pre=[".."]+[p.name for p in current_folder.iterdir()]
            subfolders="\n".join(subfolders_pre)

            sub_ui=subprocess.run(["fzf"],
                    input=subfolders,
                    text=True,
                    capture_output=True)
            
            selected_folder=sub_ui.stdout.strip()

            if selected_folder=="..":
             if current_folder==Path(current_folder.anchor):
               break
             else:
               current_folder=current_folder.parent
            else:
              current_folder=current_folder / selected_folder
              print(f"PATH: {current_folder}")
              print(f"IS FILE: {current_folder.is_file()}")
              if current_folder.is_file():
                 current_file=current_folder
                 dis=False
                 subf=False
                 print("File has been selected successfully!")
                 print("What would you like to call it : ")
                 nick=input()
                 print("Are you sure (y/n)")
                 nick_sure=input()
                 name_value=nick
                 path_value=current_file
                 marked_value=1
                 last_seen_value = datetime.now().isoformat()
                 
                 if nick_sure.strip().lower()=="y":
                    print("File has been successfully marked")
                    cur.execute("""INSERT INTO file_info (path,name, is_marked,last_seen)
                                     VALUES(?,?,?,?)""",
                                     (path_value,
                                      name_value,
                                      marked_value,
                                      last_seen_value))
                    conn.commit()
                    break
                 elif nick_sure.strip().lower()=="n":
                    print("User has cancelled the marking procedure!")
                    break
                 else:
                    print("Inalid Response please choose a correct option")
                 

                 return

                 

file_prober()
