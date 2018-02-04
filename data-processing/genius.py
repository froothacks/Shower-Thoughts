import requests
import pickle

from itertools import cycle
from itertools import repeat

TIMEOUT = 3

accessTokens = cycle([
"J3n5zoDA27CGDoxTlLPsmZW8L_PONjoI8kQ_yWVJkPvpy1ea4Ya8wOSJcG1Bj6bl",
"dQTg_qDehFh9HRvT6f7fjDeuSEk21_dwGHA_9fVrDbAmMr9M4bYajdxLBlqZ61NS",
"OEk9GKp2IME7SC3Cg73CgHOxasXoHKG6aJvTedwBhO6F_ehAcdBBZcOBpSuvanoD",
"hoCZaYGJl0FKGT0y1vzMjQeRv3FcMoHzn32RrU0NGkaBuRYlshvD0y_dTJ6tyfLN",
"Y20TirpvvtLDz2R096md8X7BsMXJEDEnBlemAv3Wt1lRp4O_xPx_KfvzNsw01Pu1",
"D_Q1Pzj32GWS46juqOHbzw2VnKA4uzakqMH9neygpNmqG4GZc5uUcxtjqByoFy5G",
"a-_VSv6ZVjyqoNoDhi1pg-qc4w5AKIPOKVdFXIb1Ya6lN7ynd9HYRnZPC770ud2P",
"qd13PAzX1RMt3dIh1J_IzR7E4tQQ9WSoyUrAknCRqLhWCHdXZ_MoFIo_b0WGXRGo",
"O-7AjYPSZamvhT8IEF9uuJvV_8X5Z1WAmL5O1fS6rWHYVgd0p543_b1n29JAM9-C",
"6hZzhYLMFyj9pm4CEsvn-CSY-JnqG2c4ZZFLd73KMD4UpBdkiSdFT_uqM55nwMfi",
"scnog-qar9a3c89C2CSA1freB2t_Tb9AWo1-p5RbBm2HYYYgTOkaYWvqw-bDccM2",
"mk2TQDC82NzMA1G82kO26Ys440Xm8vGiLxywdeNpF-6DMenz429YQN4Y2D-yS-IB",
"X9gO6RhohUO3TkBDJ4AGgVtLy2XMWa3PxWehUkrrTZ_ggExMHsNXLcq24A4kk72F",
"vHsVUMXi0tq7zHMVaGx9wac1oLep52zZ9DCdjyM4xM1jCz1B9hjdAOl4JzEyKXEH",
"vF3iKcTZQ4jKLKtvLzumH7fdTEJtMRuYcUZCMYn8ohVc2W7au52hsO312T4YQGn2",
"tHUTCq9__27auB-V3yd1UnMNLwzX0QzwE0ZcVC5cG7g_f9msZv3fRJ7H_ypcAeTf"
])

# accessTokens = repeat("lmlQpx5geldh67aJ2YqHjIG5UGtDNrqwMb9-94N-G72ICN0OjsNGi7a-T5G_6lEE")

def nextHeader():
    return {"Authorization": "Bearer " + next(accessTokens)}

def getWithRetry(*args, **kwargs):
    try:
        return requests.get(*args, **kwargs, timeout=TIMEOUT)
    except requests.exceptions.Timeout as e:
        print("TIMEOUT - Retrying")
        return getWithRetry(*args, **kwargs)
    except Exception as e:
        print(type(e))
        print(e)

songAnnotations = []

songIndex = 0
runningTotal = 0


with open("songs-unique.txt") as f:
    songTitles = f.read().split("\n")
    for songTitle in songTitles:
        try:
            songIndex += 1
            print(songIndex, songTitle, end=": ")

            # Get song id from title
            params = {"q": songTitle}
            res = getWithRetry("https://api.genius.com/search", headers=nextHeader(), params=params)
            json = res.json()
            hits = json["response"]["hits"]
            if len(hits) == 0:
                print("Song not found")
                continue

            songid = hits[0]["result"]["id"]

            # Get song annotations from song id
            params = {"song_id": songid, "per_page": 50, "text_format": "plain"}
            res = getWithRetry("https://api.genius.com/referents", headers=nextHeader(), params=params)
            json = res.json()
            referents = json["response"]["referents"]

            count = 0
            for referent in referents:
                lyric = referent["fragment"]
                annotation = referent["annotations"][0]["body"]["plain"]
                votes = referent["annotations"][0]["votes_total"]
                verified = referent["annotations"][0]["verified"]
                if votes >= 40 or verified:
                    count += 1
                    runningTotal += 1
                    songAnnotations.append((lyric, annotation))

            print("%d out of %d (Total: %d)" % (count, len(referents), runningTotal))

            if runningTotal >= 30000:
                break

        except Exception as e:
            print(e)


print(len(songAnnotations))

with open("annotations.dat", "wb") as f:
    pickle.dump(songAnnotations, f)

print("Done!")
