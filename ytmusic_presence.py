from pypresence import Presence
import pygetwindow as gw
import time
import win32gui

client_id = 1385959866262229084
rpc = Presence(client_id)
rpc.connect()

last_title = None
last_update_time = 0
presence_active = False

def extract_song_info(title):
    song_info = title.replace(" - YouTube Music", "")
    try:
        song, artist = song_info.split(" - ", 1)
    except ValueError:
        song, artist = song_info, "Unknown"
    return song.strip(), artist.strip()

def detect_youtube_music_title():
    windows = gw.getAllTitles()
    for title in windows:
        if " - YouTube Music" in title:
            return title
    return None

while True:
    try:
        title = detect_youtube_music_title()
        current_time = time.time()

        if title:
            if title != last_title:
                song, artist = extract_song_info(title)
                print(f"Now Playing: {song} by {artist}")
                rpc.update(
                    details=f"🎵 {song}",
                    state=f"👤 {artist}",
                    large_image="youtube",
                    start=current_time
                )
                last_title = title
                last_update_time = current_time
                presence_active = True
        else:
            # If nothing found for > 30 seconds, clear status
            if presence_active and current_time - last_update_time > 30:
                print("No song playing or tab not found for 30s. Clearing presence.")
                rpc.clear()
                last_title = None
                presence_active = False

        time.sleep(5)

    except Exception as e:
        print(f"[Error] {e}")
        time.sleep(1)
