import glob
import sys
import os
import shutil
import unicodedata
import re

path = sys.argv[1].rstrip(r"\/")

invalid_chars = re.compile(r"[~*:\"!?&$#]")
number_format = re.compile(r"([0-9]+)-?([0-9]+)? (.*)")

find = []
replace = []


def normalise(path):
    for root, _, files in os.walk(path, topdown=False):
        if os.path.basename(root)[0] == ".":
            continue
        for file in files:
            oldpath = os.path.join(root, file)
            newpath = re.sub(
                invalid_chars,
                "",
                unicodedata.normalize("NFKD", oldpath)
                .encode("ascii", "ignore")
                .decode("ascii"),
            ).strip()
            (name, ext) = os.path.splitext(os.path.basename(newpath))
            if not os.path.basename(newpath).strip()[:-4]:
                newpath = os.path.join(os.path.dirname(newpath), "UNKNOWN" + ext)
            else:
                m = number_format.match(name)
                if m:
                    name = m[1]
                    if m[2] is not None:
                        name = m[2]
                    name += f". {m[3]}{ext}"
                    newpath = os.path.join(os.path.dirname(newpath), name)

            dirs = list(os.path.split(newpath))
            while dirs[0] != path:
                d = os.path.split(dirs[0].rstrip("."))
                dirs.insert(1, d[1])
                dirs[0] = d[0]
            newpath = os.path.sep.join(dirs)

            if newpath != oldpath:
                find.append(oldpath[len(path) + 1 :])
                replace.append(newpath[len(path) + 1 :])
                newdir = os.path.dirname(newpath)
                if not os.path.exists(newdir):
                    os.makedirs(newdir)
                shutil.move(oldpath, newpath)

        if not os.listdir(root):
            os.rmdir(root)


normalise(path)

for playlist_path in glob.glob(os.path.join(path, "*.m3u")):
    with open(playlist_path, "r") as file:
        playlist = file.read()
    for f, r in zip(find, replace):
        playlist = playlist.replace(f, r)
    with open(playlist_path, "w") as file:
        file.write(playlist)

