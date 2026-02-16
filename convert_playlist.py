from tinytag import TinyTag
import pickle
import csv
import os
import sys
import re
from pathlib import Path
import hashlib

AUDIO_EXTS = {".mp3", ".flac", ".m4a", ".wav", ".ogg"}

parens = re.compile(r"\(([^)]+)\)")
dashes = re.compile(r" - .*")
feat = re.compile(r"(ft\.|feat\.) .*")

nonletters = re.compile(r"[^a-z ]")

commas = re.compile(r", .*")

def hash_music_library(music_dir: Path):
    hash = hashlib.new("md5")
    for root, dirs, files in os.walk(music_dir, topdown=True):
        dirs[:] = [d for d in dirs if d[0] != "."]
        for name in files:
            path = Path(root) / name
            if path.suffix.lower() in AUDIO_EXTS:
                hash.update(bytes(path))
    return hash.hexdigest()

def index_music_library(music_dir: Path):
    index = []
    for root, dirs, files in os.walk(music_dir, topdown=True):
        dirs[:] = [d for d in dirs if d[0] != "."]
        for name in files:
            path = Path(root) / name
            if path.suffix.lower() in AUDIO_EXTS:
                tags = TinyTag.get(path)
                index.append(
                    {
                        "path": path,
                        "key": f"{tags.artist} {tags.other['band'] if 'band' in tags.other else ''} {tags.title}".lower(),
                    }
                )
    return index


def find_track(track_name, artist_names, library_index):
    track_name = track_name.lower()
    artist_names = artist_names.lower()

    tracks = [
        i
        for i in [
            track_name,
            re.sub(parens, "", track_name).strip(),
            re.sub(dashes, "", track_name).strip(),
            re.sub(dashes, "", re.sub(parens, "", track_name)).strip(),
            re.sub(parens, "", re.sub(dashes, "", track_name)).strip(),
            re.sub(feat, "", track_name).strip(),
            re.sub(nonletters, "", track_name).strip(),
        ]
        if i
    ]
    artists = [
        i
        for i in [
            artist_names,
            re.sub(commas, "", artist_names).strip(),
            re.sub(nonletters, "", artist_names).strip(),
        ]
        if i
    ]

    for entry in library_index:
        has_artist = False
        for artist in artists:
            if artist in entry["key"]:
                has_artist = True
                break
        has_track = False
        for track in tracks:
            if track in entry["key"]:
                has_track = True
                break
        if has_artist and has_track:
            return entry["path"]

    for entry in library_index:
        for track in tracks:
            if track in entry["key"]:
                return entry["path"]

    return None


def main(csv_path, music_dir, output_m3u):
    print("Playlist", csv_path)
    if output_m3u[-4:] == ".csv":
        output_m3u = output_m3u[:-4] + ".m3u"
    csv_path = Path(csv_path)
    music_dir = Path(music_dir)
    output_m3u = Path(output_m3u)

    library_hash = hash_music_library(music_dir)
    library_index = []
    should_reindex = False
    if os.path.exists(music_dir / "musdb.pickle"):
        with open(music_dir / "musdb.pickle", "rb") as file:
            (old_hash, library_index) = pickle.load(file)
            if old_hash != library_hash:
                should_reindex = True
    else:
        should_reindex = True

    if should_reindex:
        print("Indexing music library...")
        library_index = index_music_library(music_dir)
        with open(music_dir / "musdb.pickle", "wb") as file:
            pickle.dump((library_hash, library_index), file)
        print("Done.")

    found = []
    missing = []

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            track = row["Track Name"]
            artists = row["Artist Name(s)"]

            match = find_track(track, artists, library_index)
            if match:
                found.append(match)
            else:
                missing.append(f"{artists} – {track}")

    with output_m3u.open("w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for path in found:
            f.write("." + str(path.resolve())[len(str(music_dir.resolve())) :] + "\n")

    print(f"Playlist written to: {output_m3u}")
    print(f"Found tracks: {len(found)}")
    print(f"Missing tracks: {len(missing)}")

    if missing:
        print("\nMissing:")
        for m in missing:
            print("  ", m)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: <playlist.csv> <music_dir> <output.m3u>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])

