import sys
import os
import shutil
import unicodedata
import re

path = sys.argv[1]

invalid_chars = re.compile(r"[~*:\"!?&]")


def normalise(path):
    for name in os.listdir(path):
        old_path = os.path.join(path, name)
        if os.path.isdir(old_path):
            new_name = re.sub(
                invalid_chars,
                "",
                unicodedata.normalize("NFKD", name)
                .encode("ascii", "ignore")
                .decode("ascii"),
            ).strip()
            if not new_name.strip():
                new_name = "UNKNOWN"
            new_path = os.path.join(path, new_name)

            if new_name != name:
                if os.path.exists(new_path):
                    for file in os.listdir(old_path):
                        new_file = os.path.join(new_path, file)
                        old_file = os.path.join(old_path, file)
                        if os.path.isfile(old_file) and not os.path.exists(new_file):
                            shutil.move(old_file, new_file)
                    os.rmdir(old_path)
                else:
                    os.rename(old_path, new_path)
            normalise(new_path)


normalise(path)

