import os


def count_file_and_lines(start, lines=0, files=0, begin_start=None):

    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isfile(thing):
            if thing.endswith(".py"):
                files += 1
                with open(thing, "r") as f:
                    newlines = f.readlines()
                    newlines = len(newlines)
                    lines += newlines

                    if begin_start is not None:
                        reldir_of_thing = "." + thing.replace(begin_start, "")
                    else:
                        reldir_of_thing = "." + thing.replace(start, "")

    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isdir(thing):
            files, lines = count_file_and_lines(
                thing, lines, files=files, begin_start=start
            )

    return files, lines