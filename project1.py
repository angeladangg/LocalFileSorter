
from pathlib import Path
import os
import shutil
import os.path, time
#test: R /Users/angeladang/Desktop/ICS week 2
#      D /Users/angeladang/Documents
def print_lines_in_d(dir_string):
    '''dir_string: given directory in string form
    stores all files from given directory in sorted fashion'''
    p = Path(dir_string) 
    if p.is_dir():
        files_list = sorted([str(x).strip() for x in p.iterdir()])
    return files_list

def print_lines_in_r(dir_string):
    '''dir_string: given directory in string form,
        return a sorted list of file names'''
    '''recursively print files in directory and its subdirectories and so on'''
    files_list, sub_list = [], []
    p = Path(dir_string)
    if p.is_dir():
        for x in p.iterdir():
            if x.is_file():
                files_list.append(str(x).strip())
            elif x.is_dir():
                sub_list.append(str(x))
    files_list.sort()
    for element in sub_list:
        files_list += print_lines_in_r(element)
    
    return files_list

#input 2 functions:
def matched_names(l, target):
    '''finds filenames that exactly match the target
    l: sorted list from first input, target: requested search target'''
    qualified = [i for i in l if os.path.basename(i) == target]
    
    return qualified

def extension(l, target):
    '''qualify files that match requested extension
    l: sorted list from first input, target: requested extension'''
    qualified = [i for i in l if os.path.splitext(i)[-1] and os.path.splitext(i)[-1].strip(".") == target.strip(".")]
    return qualified

def text_in_file(l, target):
    '''qualify files if requested content is in file's text content
    l: sorted list from first input, target: requested content'''
    qualified = []
    for file in l:
        try:
            opened_file = open(file)
            content = opened_file.read()
            if target in content:
                qualified.append(file)
        except:
            pass
        
        finally:
            opened_file.close()
    return qualified

def lesser(l, target):
    '''qualify files that are only lesser than the threshold in bytes
    l: sorted list from first input, target: requested threshold'''
    assert type(target) is int
    assert target > 0
    qualified = [ i for i in l if os.path.getsize(i) < target]
    return qualified

def greater(l, target):
    '''qualify files that are only greater than the threshold in bytes
    l: sorted list from first input, target: requested threshold'''
    assert type(target) is int
    assert target > 0
    qualified = [ i for i in l if os.path.getsize(i) > target]
    return qualified

#input 3 functions:
def print_first_line(l):
    '''if it's a file, print the first line; if not, quietly skip'''
    for file in l:
        try:
            opened_file = open(file)
            print(opened_file.readline().strip("\n"))
        except:
            print("NO TEXT")
            pass
        finally:
            opened_file.close()

def make_duplicate(l):
    '''duplicate file into same directory, attach .dup at end of file name'''
    for file in l:
        shutil.copy(file, Path(str(file) + '.dup'))

def modify_time(l):
    '''changes last opened' time to current time'''
    for file in l:
        os.utime(file, None)

def print_it(l):
    '''helper function to print lines of textfiles in a list of files'''
    for line in l:
        print(line)

if __name__ == "__main__":
    #input 1:
    while True:
        the_dir = input()
        file_type = the_dir[0:2]
        path = the_dir[2:]
        if file_type == "D ":
            if Path(path).exists():
                files_list = print_lines_in_d(str(path))
                print_it(files_list)
                break
            else:
                print("ERROR")
        elif file_type  == "R ":
            if Path(path).exists():
                files_list = print_lines_in_r(str(path))
                print_it(files_list)
                break
            else:
                print("ERROR")
        else:
            print("ERROR")
    # files_list: has all the sorted files
    #input 2:
    while True:
        narrow_input = input()
        command = narrow_input[0:2]
        search = narrow_input[2:]
        assert type(search) is int and search > 0 or type(search) is str
        
        if narrow_input == "A":
                #all files are considered interesting
                refined_list = files_list
                print_it(refined_list)
                break
        elif len(narrow_input) >= 3:
            if command == "N ":
                refined_list = matched_names(files_list, search)
                print_it(refined_list)
                break
            elif command == "E ":
                refined_list = extension(files_list, search)
                print_it(refined_list)
                break        
            elif command == "T ":
                refined_list = text_in_file(files_list, search)
                print_it(refined_list)
                break
            elif command == "< " and search.isalpha() == False and int(search) > 0:
                refined_list = lesser(files_list, int(search))
                print_it(refined_list)
                break
            elif command == "> " and search.isalpha() == False and int(search) > 0:
                refined_list = greater(files_list, int(search))
                print_it(refined_list)
                break
            else:
                print("ERROR")
        else:
            print("ERROR")
        
    #refined_list: a list of strings of file names after 2nd filter
    #input 3:
    while True:
        final_input = input()
        if final_input == "F":
            print_first_line(refined_list)
            break
        elif final_input == "D":
            make_duplicate(refined_list)
            break
        elif final_input == "T":
            modify_time(refined_list)
            break
        else:
            print("ERROR")
