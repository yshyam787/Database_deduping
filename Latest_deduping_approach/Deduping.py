# Deduping the database using the dededupe library
import os #For accessing the directories. 
import modin.pandas as pd
import pandas_dedupe



if __name__ == '__main__':
    #num_cores = None #to prevent from multi-processing error.
    
    #Automate reading all the folders by aceessing its paths. (in the form of function)
    #Create dictionary with countries with file_names. (also as a function in the form of dictionary)
    #Create a function returning the dataframe based on the keys and values of dictionary (3 arguments, country, its path, and import/export flags)
    # Crate a fuction for training the data  and store in a dataframe with clusters and cluster confidence.
        # ---A function to delete the clusters with blank values.
    
    export_data = pd.read_excel('Book1.xlsx', sheet_name = 'Exports')  # reading the excel file
    export_df = pd.DataFrame(export_data)  # importing the data to the dataframe
    
    columns = {}
    for i in export_df.columns:
        columns = columns | {i: i.strip()} #renaming the columns by removing the spaces at the start/end of columns
    export_df.rename(columns=columns, inplace=True) #renaming the columns and removing the spaces. Also, making the modificiation valid.
    #Deduping the database
    export_df2 = pandas_dedupe.dedupe_dataframe(export_df, ['Shipper', 'Shipper Address'])
        
    import_data = pd.read_excel('Book1.xlsx', sheet_name = 'Imports')  # reading the excel file
    import_df = pd.DataFrame(import_data)  # importing the data to the dataframe
    
    columns = {}
    for i in import_df.columns:
        columns = columns | {i: i.strip()} #renaming the columns by removing the spaces at the start/end of columns
    import_df.rename(columns=columns, inplace=True) #renaming the columns and removing the spaces. Also, making the modificiation valid.
    #Deduping the database
    import_df2 = pandas_dedupe.dedupe_dataframe(import_df, ['B/L No', 'Shipper', 'Shipper Address', 'Consignee', 'Consignee Address', 'WGT(KGS)','PKG','PKG Unit', 'CMDT Code', 'CMDT'])
        
    with pd.ExcelWriter('Processesed.xlsx') as writer: #writing data to new file with two sheets.
        export_df.to_excel(writer, sheet_name='Export')
        export_df2.to_excel(writer, sheet_name='Deduped_export')
        import_df.to_excel(writer, sheet_name='Import')
        import_df2.to_excel(writer, sheet_name='Deduped_import')