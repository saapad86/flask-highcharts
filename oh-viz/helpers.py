from collections import OrderedDict
import pandas as pd
import numpy as np
import datetime


def json_series(index,data):
    return pd.io.json.dumps(list(zip(index.tolist(),data.tolist())))

def extract_column(df,index,column):
    return [list(a) for a in zip(index, df[column])]

def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

def extract_timeseries_data(df, columns, index_col='activity_dt'):
    '''
    INPUT: DataFrame, data columns (LIST of STRINGS), index column (STRING)
    OUTPUT: data (LIST of LISTS)

    Creates a list of timeseries data, where each index is a unix timestamp and
    the associated value is a datapoint from the specified column. Lists can be
    unpacked by indexing or by naming. The index is assumed to be named "activity_dt"
    unless otherwise specified using the index_col argument.

    ex.
    data1, data2 = extract_timeseries_data(mydataframe, ['col1', 'col2'])
    ~ or ~
    data = extract_timeseries_data(mydataframe, ['col1', 'col2'], 'batch_dt')
    data[0] = [list of data]
    data[1] = [list of data]
    '''

    # check unique dates
    if not df[index_col].is_unique:
        print("Please pass a dataframe with unique dates (i.e. 1 row per date)")
        return None

    # check is datetime
    if df[index_col].dtype != '<M8[ns]':
        df[index_col] = pd.to_datetime(df[index_col])

    # Create a datetime index, filling in gaps for days with missing data
    df = df.set_index(index_col, drop=False)
    df = df.reindex(pd.date_range(start=df[index_col].min(),end=df[index_col].max(),fill_value=0))
    # Create a javascript-friendly datetime (ms) from our pandas datetime (ns)
    js_datetime = map(unix_time_millis, df.index)
    # Highcharts does not like NAs...
    df.fillna(0, inplace=True)

    # if only 1 column, return list instead of list of lists
    if len(columns) == 1:
        col = columns[0]
        return extract_column(df, js_datetime, col)

    output_data = []
    for col in columns:
        output_data.append(extract_column(df, js_datetime, col))

    return output_data

def build_table(df, row_column_matches, current_segment, segment_variable, time_variable, categories=None):
    '''
    INPUT: df (Pandas DataFrame),
           row_column_matches (LIST of tuples mapping table labels to df column names; see below),
           current_segment (STRING),
           segment_variable (STRING) -- column name of segment variable,
           time_variable (STRING) -- column name of df where time period variable (for sparklines) is stored,
           categories (LIST of STRINGS) -- labels for sparkline x-Axis/hover tips
    OUTPUT: data for table template (DICT), labels (LIST)

    Properly formats data for a table with sparklines in High Charts.

    row_column_matches = [
    (tablerow_1, {label1 : name of column 1, label2 : column 2, label3 : column 3}),
    (tablerow_2, {label1 : name of column 1, label2 : column 2, label3 : column 3}),
    ....
    (tablerow_n, {label1 : name of column 1, label2 : column 2, label3 : column 3})
    ]
    '''

    df.fillna(0, inplace=True)
    df.sort_values(by=time_variable, inplace=True)
    df= df.set_index([segment_variable, time_variable])
    data_dict = OrderedDict()

    for pair in row_column_matches:
        row = pair[0]
        data_dict[row] = {}
        for label, col in pair[1].iteritems():
            data_dict[row][label] = df.loc[current_segment][col].values

    if categories:
        categories.insert(0, '_') # place holder so highcharts doesn't skip first item
    else:
        temp = list(df[time_variable].unique())
        categories = ["_"]
        categories.extend(temp)

    return data_dict, categories
