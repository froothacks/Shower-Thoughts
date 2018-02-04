import pickle

with open("annotations.dat", "rb") as f:
	annotations = pickle.load(f)

print(annotations[0])
print(len(annotations))