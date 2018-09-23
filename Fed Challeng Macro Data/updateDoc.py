from dataSeries import dictSeries
from fredapi import Fred
import pandas as pd
import os

fred = Fred(api_key='129c1c0d602287cb65291a2166295ce1')

def pctChange(series_id, freq):
    if freq == 'M':
        i = -13
    elif freq == 'Q':
        i = -5
    elif freq == 'A':
        i = -2
    elif freq == 'D':
        i = -366
    series = fred.get_series(series_id = series_id)
    value_n = series.iloc[-1]
    value_o = series.iloc[i]
    value = ((value_n - value_o) / value_o) * 100
    value = ('%.2f' % value)

    return value

def change(series_id, freq):
    if freq == 'M':
        i = -13
    elif freq == 'Q':
        i = -5
    elif freq == 'A':
        i = -2
    elif freq == 'W':
        i = -53
    series = fred.get_series(series_id = series_id)
    value_n = series.iloc[-1]
    value_o = series.iloc[i]
    value = value_n - value_o
    value = ('%.2f' % value)

    return value

def sepPull(var, series_id):
    series = fred.get_series(series_id = series_id)
    if var == 'SEP2018':
        value = series.iloc[-3]
    elif var == 'SEP2019':
        value = series.iloc[-2]
    elif var == 'SEP2020':
        value = series.iloc[-1]

    freq = 'A'

    return value, freq


def dataPull(series_id, pct_change):
    df_search = fred.search(series_id)
    freq = str(df_search.iloc[0,1])

    if pct_change == 0:
        series = fred.get_series(series_id = series_id)
        value = str(series.iloc[-1])
    elif pct_change == 1:
        value = pctChange(series_id,freq)
    elif pct_change == 2:
        value = change(series_id,freq)

    return value, freq

def dataWriter(var, value, freq, unit):
    with open('USMacroSummary.txt','r+') as file:
        doc = file.readlines()
        updated_lines = []

        for line in doc:
            if var in line:
                line = line.split('=')
                line[1] = f' {value} ({freq} , {unit})\n'
                line = '='.join(line)
                updated_lines.append(str(line))
            else:
                updated_lines.append(str(line))

        updated_lines = [l.replace('\x00','') for l in updated_lines]

        file.seek(0)
        file.truncate()
        file.writelines(updated_lines)
        file.close()



def main():
    for k,v in dictSeries.items():
        series_id = v[0]
        pct_change = v[1]

        if pct_change == 1:
            unit = 'Percent Change'
        elif pct_change == 2:
            unit = 'Change'
        else:
            if v[2] == 1:
                unit = 'Percent Change'
            else:
                if k in ['Savings Rate','U-3 UR','U-6 UR','LFPR','Sperations','Quits','5 year, 5 year forward','Michigan','TIPS','Effective ffr','Short-Term Treasury Yield(3-month)','Long-Term Treasury Yield(10 year)','S&P 500 Index','NAIRU']:
                    unit = 'Percent'
                elif k in ['Inventory to Sales Ratio','i']:
                    unit = 'Ratio'
                else:
                    unit = 'Level'

        if k in ['SEP2018','SEP2019','SEP2020']:
            value, freq = sepPull(k, series_id)
        else:
            value, freq = dataPull(series_id, pct_change)

        dataWriter(k, value, freq, unit)

    os.startfile('USMacroSummary.txt')




if __name__ == '__main__':
    main()
