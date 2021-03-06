import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

## TODO: Functions for cleaning headers, creating new time variables, show variables with missing values, 


def clean_headers(df, remove_whitespace=True, replace_dash=False, lowercase=False, uppercase=False):
    '''Function that formats the column headers of a dataframe.
    Arguments:
        df : Pandas DataFrame
            Dataframe to be formatted. 
        remove_whitespace : bool
            Removes whitespaces from column headers.
        replash_dash : bool
            Replaces dashes in column headers with underscores.
        lowercase : bool
            Changes column headers to lowercase.
        uppercase : bool
            Changes column heaedrs to uppercase.
        
    Returns:
        df : Pandas DataFrame
            Formatted dataframe.
    
    '''
    if remove_whitespace:
        df.columns = df.columns.str.replace(' ', '')
        print('Removing whitespaces ...')
    
    if replace_dash:
        df.columns = df.columns.str.replace('-', '_')
        print('Replacing dashes with underscores ...')

    if lowercase:
        df.columns = df.columns.str.lower()
        print('Changing to lower case ...')
    
    if uppercase:
        df.columns = df.columns.str.upper()
        print('Changing to upper case ...')
    
    print('Dataframe column headers have been formatted.')

    return df
    

def check_missing(df):
    '''Function that shows the variables that have missing values and their percentage of total missing.

    Arguments:
        df : Pandas DataFrame
            Dataframe whose variables are to be checked.

    Returns:
        missing_percentages : Pandas Series
            Descending sorted series with variables as index and their respective missing percentage as values.        

    '''
    print(f'The dataframe has {df.shape[1]} variables.')

    missing_percentages = df.isnull().mean().sort_values(ascending=False) * 100
    missing_percentages = missing_percentages.loc[missing_percentages > 0]

    if missing_percentages.size > 0:
        print(f'The dataframe has {missing_percentages.size} variables that have missing data.')
    
    else:
        print('The dataframe has no variables that are missing values.')

    return missing_percentages


def check_negative(df, exclude_vars=[]):
    '''Function that check the numeric columns and determines if they are all non-negative.
    Arguments:
        df : Pandas DataFrame
            Dataframe to be checked.
        exclude_vars : list
            List of variables names to exclude from the check.
    '''
    numeric_vars = df.select_dtypes(include='number').columns.to_list()
    vars_to_check = [var for var in numeric_vars if var not in exclude_vars]
    neg_values = [] 

    for var in vars_to_check:
        neg_values.append(any(df[var] < 0))

    results = pd.DataFrame.from_dict(
        dict(zip(vars_to_check, neg_values)),
        orient='index',
        columns=['NegativeValues']
    )

    if results.NegativeValues.mean() > 0:
        neg_vars_count = results.NegativeValues.loc[results.NegativeValues == 1].count()
        print(f'There are {neg_vars_count} variables with negative values.')
        print('To view variables, please save results.')
    
    else:
        print('There are no numeric variables with negative values.')
    
    return results
    




def create_time_vars(df, time_var, year=True, month=True, day=True, season=True, drop=True):
    '''Function that creates additional time-related features by extracting them from a datetime series (colunn).
    Arguments:
        df : Pandas DataFrame
            Dataframe with the datetime variable.
        time_var : str
            Variable name. Variable must be in datetime format.
        year : bool
            Creates a new year column in the dataframe.
        month : bool
            Creates a new month column in the dataframe.
        day : bool
            Creates a new day of week column in the dataframe.
        season : bool
            Creates a new season column in the dataframe.
        drop : bool
            Drop time_var which was used to extract the other features.
    
    Returns:
        df : Pandas DataFrame
            Dataframe with added time variables.

    '''
    ## TODO : Raise exceptions for wrong data types.

    if year:
        df['year'] = df[time_var].dt.year
        df.year = df.year.astype('category')

    if month:
        df['month'] = df[time_var].dt.month_name()
        df.month = df.month.astype('category')

    if day:
        df['day'] = df[time_var].dt.day_name()
        df.day = df.day.astype('category')

    if season:
        seasons = [
            'Winter', 'Winter', 'Spring', 'Spring', 'Spring', 'Summer',
            'Summer', 'Summer', 'Autumn', 'Autumn', 'Autumn', 'Winter'
        ]

        month_to_season = dict(zip(range(1,13), seasons))
        df['season'] = df[time_var].dt.month.map(month_to_season)
        df.season = df.season.astype('category')

    if drop:
       df = df.drop(time_var, axis=1)
       print('Datetime variable has been dropped.')
    
    return df


def convert_to_categorical(df, add_vars=[]):
    '''Function to change variable datatypes to categorical data type.
    Arguments:
        df : Pandas DataFrame
            Dataframe to format.
        add_vars : list of variable names 
            Additional variables to change their data type to categorical.
        
    Returns:
        df : Pandas DataFrame
            Formated Dataframe.

    '''
    cat_vars = df.select_dtypes(exclude='number').columns.to_list()
    
    if len(add_vars) > 0:
        [cat_vars.append(x) for x in add_vars]
    
    for var in cat_vars:
        df[var] = df[var].astype('category')
    
    return df


def label_encode(df,exclude_list=[]):
    ''' Funciton that label encodes categorical varaibles that have two or less unique categories.
    Arguments:
        df : Pandas DataFrame
            Dataframe of which its variables will be encoded.
        exclude_list : list
            List of variable names to be excluded from the encoding.
    
    Returns:
        df : Pandas DataFrame
            Dataframe with variables encoded.
    ''' 
    cat_vars = df.select_dtypes(include='category').columns.to_list()
    vars_to_encode = [x for x in cat_vars if x not in exclude_list]
    encoder = LabelEncoder()

    for var in vars_to_encode:
        if len(list(df[var].unique())) <= 2:
            df[var] = encoder.fit_transform(df[var])

    print(f'A total of {len(vars_to_encode)} variables have been encoded.')

    return df

    
    