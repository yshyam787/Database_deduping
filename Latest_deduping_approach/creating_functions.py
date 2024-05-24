import os
import pandas_dedupe
import pandas as pd
from collections import defaultdict    
from consts import target_data, config_base, result_base

#for example, the paths_of_china_Book1.xlsx as file list is the one argument and 'import_variable' as the dataframe type  is another argument.
def get_dataframe(filelist:list, df_type:str):
    if len(filelist)>1: #if there are more than one paths_of_china_Book1.xlsx then below code operates/check_multiple_file_paths in china_Book1.xlsx.
        for f in filelist: #Looping around multiple paths_of_china_Book1.xlsx. it has both import and export .xlsx files
            print(f)
            file = pd.ExcelFile(f) #let's say this code read china_import_Book1.xlsx file and store in file data frame. This part is used to store the excel file into the dataframe so that it can be used later on. 
            if df_type in f: #if import variable is in the path_name_of china_import_Book1.xlsx file then follow the below code.
                print("Reading import_.xlsx files of countries and importing them to the dataframe")
                df= pd.read_excel(f) #Reading from path_of_china_import_Book1.xlsx file and storing in df dataframe.
            elif df_type in file.sheet_names: #If there are no china_import_Book1.xlsx file, but import_sheets in china_import_Book1.xlsx then: read the china_import_sheets from the first item of list of path_of_china_Book1.xlsx_import_sheets.
                df= pd.read_excel(filelist[0], sheet_name=df_type) 
            else:
                continue #if there are no 'import' variable in path_china_import_Book1.xlsx, no import_sheets in china_import_Book1.xlsx in the first list, then skip the process and continue for path_china_export_Book1.xlsx files.

    #if the there are no more than one paths_of_china_Book1.xlsx, the the blelow code operates. 
    else:
        file = pd.ExcelFile(filelist[0]) #read the excel file form the paths_china_Book1.xlsx and store it in file dataframe.
        for f in file.sheet_names:
            if df_type in f:    #if the sheets_name is import then split the sheets from path_china_Book1.xlsx and store it in the 'df' dataframe.     
                df = file.parse(f)

    #precessing the stored dataframe
    renames = [c.strip() for c in df.columns] #removing the spaces and new lines from the columns
    df.columns = renames #overwriting the modified columns
    df.fillna('Unknown') #filling out the empty cells with 'Unknown'
    return df
    #returning dataframe of either the china_import_Book1.xlsy
    # x, or china_import_sheets.xlsx or the import_sheets_Book1.xlsx. The next round of  the code does the same with the export part. 

#path walking through the directory and storing key and values in the countries. 
def os_path_walk(directory:str) -> dict: #it tells the function returns the dictionary(dict).
    """
    Traverse directory with countries as subfolders

    Args:
        directory (str): [description]

    Returns:
        dict: [description]
    """
    #walk through the directory and store the available folder as countries.
    countries = next(os.walk(directory))[1]  
    ret = defaultdict(list) #whenever you need a dictionary, and each element’s value should start with a default value, use a defaultdict. Here we are creating a dictionary with default value as lists. 

    #filtering out the countries and appending it to the dictionary. 
    for root, dirs, files in os.walk(directory):
        #Getting the name of files
        for name in files: # for all the files in the directory
            for c in countries: #for all hte countries in c
                if c in root and not name.startswith('.'):# excluding .DStore files.
                    ret[c].append(os.path.join(root,name)) # we are storing the values in the dictionary where country [c] is the key and joined pathname of country folders + file names as the values.
    return ret


"""
    Deuping requires sample_size of data_feeding for training.
"""
#for deduping process:
def learning_fn(df, config_path, field_properties):
    print("Deduping the dataframe")
    #The threshold confidence is 70% and data fed to deduping is 80% and updating existing model atm.
    ret_df = pandas_dedupe.dedupe_dataframe(df, field_properties, canonicalize=True, 
                                            config_name=config_path, update_model=False, 
                                            threshold=0.7, sample_size=0.8)
    return ret_df


#     ...
if __name__ == "__main__":
    file_dict = os_path_walk(target_data) #walking through the directory of sample_database and storing the returned dictionary of country and file_pathnames as key and values. 

    #Looping through every key and values of dictionary with k,v variables to perform deduping on individual excel files.  
    for k, v in file_dict.items(): #Let's say the whole below code run for China key and paths of all Book1.xlsx (import and export) file.

        for i in ['Import', 'Export']: #Let's say the whole below code run for the "import" variable.

            #storing a function in v_resname for joining the path of result_base folder and china_imports.xlsx file
            resname = os.path.join(result_base, k+"_"+i+".xlsx") #getting the full path of china_import_Book1.xlsx in result_base folder
            if os.path.exists(resname): #if china_imports_xlsx already exists then skip this process and coninue for china_export_xlsx. If not, follow the below process.
                continue

            #print getting Imports for China.... (but the file includes both imports and exports xlsx file)
            print(f"Getting {i}s for {k}...") #formatted string literal f is a real expression evaluated at run-time. f can simply be used for printing the output.

            #Getting the dataframe from the lists of paths_of_Book1.xlsx with 'import' variable.
            df=get_dataframe(filelist=v,df_type=i)

        #store this data as df1, break the loop and continue for the export part as df2. then apply as df = concatenate([df1], [df2]). Then do some modification in the below code and here we go.

            print("Dataframe acquired...")
            #creating a variable to store the tuples of list of list.
            props = ([  ["Shipper"], ["Shipper Address"], ["Consignee"], ["Consignee Address"],
                    ])
            for p in props: #looping around the individual properties of to train the data on the basis of each properties. For example, we will train the data on the basis of shipper column on the import_china.Book1.xlsx.
                print(f"Training on {'<->'.join(p)}...")
                #joining the configuration path of china_import_shipper
                df_name = os.path.join(config_base, k+"_"+i+"_"+'-'.join(p))
                #printing the deduped database on the basis of shipper column and storing the deduped training and setting file in the Model folder.
                df = learning_fn(df, config_path=df_name, field_properties =p)
                print("Training completed")
            #After deduping the data and storing them in df, the results are stored in the result folder as china_import_xlsx file.
            with pd.ExcelWriter(resname) as f:
                df.to_excel(f, index=False)
            print("File Saved...")
            print(50*'-')
    print('done')



