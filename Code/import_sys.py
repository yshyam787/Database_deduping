'''
    1. get all the names of the files. 
    2. make the dictionary with the country as key and files as values.
'''
import os
import glob
import fnmatch
from collections import defaultdict   
path = '/Users/shyamyadav/PycharmProjects/Git/yshyam787/Code/sample_database/'
# print(next(os.walk(path))[0]) #to get the single root
# print(next(os.walk(path))[1]) #to get the single folder
# print(next(os.walk(path))[2]) # to get the single file
genpath = os.walk(path) #generates the path of single file
# print(genpath)
# loop must be used to go to the directory each time and get the different folders.
# lstfiles = [] #creating a tuple for storing the files
# lstdir = []
# for root, dir, files in os.walk(path): #it stores the root, directories, and files correspondingly
#     for name in files: #here we get the files
#         if name.endswith('.xlsx'):
#             lstfiles.append(name)          
#     for name in dir: #here we get the folders
#         if not dir==('Import' or 'Export'):
#             lstdir.append(name)

# to print out all the root, folders, and files  in sequence of every individual root.
# for root, dir, files in os.walk(path): 
#     print(root) #to print out the root of folder and subfolders inside the path directory
#     print (dir) # to print out the folders and subfolders inside the directory
#     print (files)

# to rename the excel files and store it in dictionary with the country name as their key.
lst_country = [] # for getting key
lst_excl_files = [] #for getting values
exclude = set(['Export', 'Import'])
# for root, dir, files in os.walk(path, topdown=True):
#     dir[:] = [d for d in dir if d not in exclude]
#     name = ''
#     for file in files:
#             print(name in dir)
#             if file.endswith('.xlsx'):
#                 lst_excl_files.append(file)
# print(lst_country)
# print(lst_excl_files)

for root, dirs, files in os.walk(path):
        if(os.path.basename(root) == ''):
            continue
        lst_country.append(os.path.basename(root))
        for f in files:
            if f.endswith('.xlsx'):
                lst_excl_files.append(f)
print(lst_country)
print(lst_excl_files)

def os_path_walk(directory:str) -> dict: #it tells the function returns the dictionary(dict).
    """
    Traverse directory with countries as subfolders
    Args:
        directory (str): [description]
    Returns:
        dict: [description]
    """
    countries = next(os.walk(directory))[1] #to fetch the next itemms in the walked directory.
    ret = defaultdict(list) #whenever you need a dictionary, and each element’s value should start with a default value, use a defaultdict.

    #filtering out the countries and appending it to the dictionary. 
    for root, dirs, files in os.walk(directory):
        #Getting the name of files
        for name in files:
            for c in countries:
                if c in root and not name.startswith('.'):
                    ret[c].append(os.path.join(root,name))
    return ret
print('-------------')
print(os_path_walk(path))

# print(root)
# print(lstfiles)
# print(lstdir)

