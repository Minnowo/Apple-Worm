import requests 
import os 
import re 
from contextlib import contextmanager 


OVERRIDE_EXISTING_FILES = True 

URL = [ 

    # code 
    "https://www.coolmathgames.com/0-apple-worm/play",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/src/createjs.min.js",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/src/Preloader.js",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/src/Assets.js",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/src/Worm.js",

    # assets 
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/images/CoolmathGames800x600Optimized.jpg",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/src/levels.xml",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TClick.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TDead.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TEat.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TFall.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TJump.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TMusic.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TOpen.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TPortal_1.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TPortal_2.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TRestart.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TRock.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/Tsound.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/TVzhuh.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/Vzzz2wav.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/Vzzz3wav.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/Vzzzwav.mp3",
    "https://www.coolmathgames.com/sites/default/files/public_games/24633/sounds/RockFall.mp3"
]

HEADERS = { 
    "accept": "*/*",
    "accept-encoding" : "gzip, deflate, br",
    "accept-language" : "en-US,en;q=0.9",
    "referer": "https://www.coolmathgames.com/0-apple-worm/play",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44"
}

@contextmanager
def read_write_file(path, lines, is_bytes = False):
    
    with open(path, 'r' + 'b' * is_bytes) as file:

        yield file 

    with open(path, 'w' + 'b' * is_bytes) as writer:

        writer.writelines(lines)


def main():
    
    with requests.Session() as session:

        session.headers.update(HEADERS)

        for i in URL:

            fname = i.replace("https://www.coolmathgames.com/sites/default/files/public_games/24633/", "")

            if fname.endswith("/play"):
                fname = "index.html"

            fname = os.path.join("..\\game\\", fname)

            if os.path.isfile(fname) and OVERRIDE_EXISTING_FILES:
                continue

            print(i)

            try:
                os.makedirs(os.path.dirname(fname), exist_ok=True)
            except:pass 

            try:

                response = session.get(i)

            except Exception as e:
                print(e)

            if response.status_code == 200:

                with open(fname, "wb") as writer:

                    writer.write(response.content)

        
        if os.path.isfile("..\\game\\index.html"):

            p = r"(<base\s*href=['\"](https?:)?//www.coolmathgames\.com/sites/default/files/public_games/24633/['\"]\s*\/?>)"

            lines = [] 
            with read_write_file("..\\game\\index.html", lines) as rwf:

                for line in rwf:

                    # <base href='//www.coolmathgames.com/sites/default/files/public_games/24633/' />
                    m = re.search(p, line)

                    if m:
                        lines.append(re.sub(p, "", line))
                        
                    else:
                        lines.append(line)


if __name__ == "__main__":
    main() 