import sort
import format
import sys
import os 

def write_sorted_sass(filename):
    sorted_list = sort.generate_sorted_list(filename)
    sass = format.format(sorted_list)

    with open(filename, 'w') as f:
        f.write(sass)

if __name__ == "__main__":
    path = ""
    isdir = False
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isfile(path):
            isdir = False
        elif os.path.isdir(path):
            isdir = True
        else:
            raise Exception("Path does not exist")
    else:
        raise Exception("Expected a file or directory.")

    if isdir:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                if file_path.endswith(".scss"):
                    write_sorted_sass(file_path)
    else:
        write_sorted_sass(path)
        