from fredapi import Fred
import pandas as pd
import urllib.request
import urllib
from seriesData import dict_IDs

fred = Fred(api_key='129c1c0d602287cb65291a2166295ce1')

def idToDict(series_id):
    df_search = fred.search(series_id)
    freq = df_search.iloc[0,1]
    dict_IDs[series_id].append(freq)

def seriesToDf(series_id,col_header):
    series = fred.get_series(series_id=series_id)
    df = series.reset_index()
    columns = df.columns
    df['DATE'] = df[columns[0]]
    df[col_header] = df[columns[1]]
    df = df.drop(columns,axis=1)
    return df

def main():

    df_monthly = pd.DataFrame()
    df_quarterly = pd.DataFrame()

    for ID in dict_IDs.keys():

        idToDict(ID)
        col_header = dict_IDs[ID][0]

        if dict_IDs[ID][2] == 'M':
            if df_monthly.empty:
                df_monthly = seriesToDf(ID,col_header)
            else:
                df_monthly = df_monthly.merge(seriesToDf(ID,col_header), on='DATE')

        if dict_IDs[ID][2] == 'Q':
            if df_quarterly.empty:
                df_quarterly = seriesToDf(ID,col_header)
            else:
                df_quarterly = df_quarterly.merge(seriesToDf(ID,col_header), on='DATE')

    df_monthly.to_csv('Monthly Data.csv',index=False)
    df_quarterly.to_csv('Quarterly Data.csv',index=False)


if __name__ == '__main__':
    main()
