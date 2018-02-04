

with open("songs.txt") as f:
	songs = f.read().split("\n")

setSongs = frozenset(songs)

print(len(songs))
print(len(setSongs))

with open("songs-unique.txt", "w") as f:
	for i in setSongs:
		f.write(i + "\n")

print("done")