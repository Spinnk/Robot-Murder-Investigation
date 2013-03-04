import pygame

# read the map file
def readmp(map_file_name):
    file = open(map_file_name, 'r')
    data = file.readlines()
    file.close()
    # parse map by reading the entire file, replacing display characters, and splitting up the entire string
    # change depending on how the file is actually formatted
    return [line.replace("\n", " ").replace("\r", " ").split(" ") for line in data]

