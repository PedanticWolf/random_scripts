#! /usr/env/python
import os
import hashlib
import sys

bufsize = 65536

def generate_file_digests_for(path):
	path_set = set()
	for item in os.walk(path):
		(directory, _subdirectories, files) = item
		for file in files:
			if (file[0] == '.'):
				continue
			else:
				fqFilename = os.path.join(directory, file)
				path_set.add(generate_file_digest(fqFilename, file))
	return path_set


def generate_file_digest(fqFilename, shortFilename):
	hasher = hashlib.md5()
	with open(fqFilename, 'rb') as filestream:
		fileBuffer = filestream.read(bufsize)
		while len(fileBuffer) > 0:
			hasher.update(fileBuffer)
			fileBuffer = filestream.read(bufsize)
	return (hasher.hexdigest(), fqFilename, os.path.getsize(fqFilename))


def usage():
	print "file_list.py directory1 directory2"
	print "Prints out the files present in directory1 which are NOT present in directory2"


if __name__ == "__main__":
	try:
		(_command, Path1, Path2) = sys.argv
	except:
		usage()
		exit(1)

	path_set_1 = generate_file_digests_for(Path1)
	path_set_2 = generate_file_digests_for(Path2)
	set_1_exclusives = path_set_1 - path_set_2

	print "Files present in {path1} and not in {path2}:".format(path1=Path1, path2=Path2)
	for item in set_1_exclusives:
		print item[1]