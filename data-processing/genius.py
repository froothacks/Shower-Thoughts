import requests
import pickle

geniusHeaders = {"Authorization": "Bearer J3n5zoDA27CGDoxTlLPsmZW8L_PONjoI8kQ_yWVJkPvpy1ea4Ya8wOSJcG1Bj6bl"}

songAnnotations = []

songIndex = 0
runningTotal = 0

with open("songs.txt") as f:
    songTitles = f.read().split("\n")
    for songTitle in songTitles:
        try:
            songIndex += 1
            print(songIndex, songTitle, end=": ")

            # Get song id from title
            params = {"q": songTitle}
            res = requests.get("https://api.genius.com/search", headers=geniusHeaders, params=params, timeout=1)
            json = res.json()
            hits = json["response"]["hits"]
            if len(hits) == 0:
                print("Song not found")
                continue

            songid = hits[0]["result"]["id"]

            # Get song annotations from song id
            params = {"song_id": songid, "per_page": 50, "text_format": "plain"}
            res = requests.get("https://api.genius.com/referents", headers=geniusHeaders, params=params, timeout=1)
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
