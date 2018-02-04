from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, ConceptsOptions, KeywordsOptions
from watson_developer_cloud.watson_service import WatsonApiException

from collections import defaultdict
import json
import pickle
import uuid
from pprint import pprint

MAX_RETRIES = 1

def analyzeWithRetry(maxRetries, *args, **kwargs):
    if maxRetries > 0:
        try:
            return nlu.analyze(*args, **kwargs)
        except WatsonApiException as e:
            print("[WatsonApiException - Retrying]")
            return analyzeWithRetry(maxRetries-1, *args, **kwargs)
        except Exception as e:
            print(type(e)) 
            print(e)


nlu = NaturalLanguageUnderstandingV1(
    username="922a7358-bba4-40b8-ba55-6c57345fdf57",
    password="CbCjiICaZHZO",
    version="2017-02-27")

print("Created nlu")

with open("annotations.dat", "rb") as f:
    annotations = pickle.load(f)

print("Loaded annotations: %d items" % len(annotations))

lyrics = {}
keywords = defaultdict(list)

count = 0
totalCollisions = 0

for lyric, annotation in annotations:
    try:
        count += 1

        print("%d  %-50.50r  :  %-50.50r" % (count, lyric, annotation)) # Print lyric and annotation, truncated or padded to 50 char long

        lastLen = len(keywords)

        uid = uuid.uuid3(uuid.NAMESPACE_DNS, lyric)
        lyrics[uid] = lyric

        response = analyzeWithRetry(MAX_RETRIES,
            text=annotation[:9999],
            features=Features(
                concepts=ConceptsOptions(
                    limit=50),
                keywords=KeywordsOptions(
                    emotion=False,
                    sentiment=False,
                    limit=50)))

        words = []
        for entry in response["concepts"]:
            keyword = entry["text"].lower()
            if entry["relevance"] > 0.5 and uid not in keywords[keyword]:
                keywords[keyword].append(uid)
                words.append(keyword)

        for entry in response["keywords"]:
            keyword = entry["text"].lower()
            if entry["relevance"] > 0.5 and uid not in keywords[keyword]:
                keywords[keyword].append(uid)
                words.append(keyword)

        collisions = lastLen + len(words) - len(keywords)
        totalCollisions += collisions
        print("{%-60.60s} (%d items) Collisions: %d" % (", ".join(words), len(words), collisions))
    except Exception as e:
        print(e)

try:
    print("Lyrics: %d items" % len(lyrics))
    print("Keywords: %d items" % len(keywords))
    print("Collisions: %d (%.2f)" % (totalCollisions, totalCollisions/len(keywords)))
except:
    pass

with open("lyrics.dat", "wb") as f:
    pickle.dump(lyrics, f)

with open("keywords.dat", "wb") as f:
    pickle.dump(keywords, f)

print("Written to files")
print("Done!")
