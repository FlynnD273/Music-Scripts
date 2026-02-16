import sys
import os
import shutil
import unicodedata
import re

path = sys.argv[1]

invalid_chars = re.compile(r"[~*:\"!?&]")


def normalise(path):
    for root, _, files in os.walk(path, topdown=False):
        for file in files:
            oldpath = os.path.join(root, file)
            newpath = re.sub(
                invalid_chars,
                "",
                unicodedata.normalize("NFKD", oldpath)
                .encode("ascii", "ignore")
                .decode("ascii"),
            ).strip()
            if not os.path.basename(newpath).strip()[:-4]:
                newpath = os.path.join(os.path.dirname(newpath), "UNKNOWN" + os.path.splitext(newpath)[1])

            if newpath != oldpath:
                newdir = os.path.dirname(newpath)
                if not os.path.exists(newdir):
                    os.makedirs(newdir)
                shutil.move(oldpath, newpath)

        if not os.listdir(root):
            os.rmdir(root)

normalise(path)

