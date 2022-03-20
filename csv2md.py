#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import os
import pandas as pd

args = []

def main():
    global args
    args = parse_args()

    df = pd.read_csv(filepath_or_buffer=args.csv, encoding="utf-8", sep=",")
    # print(df)
    
    df2 = df.sort_values('対戦日は？(省略すると本日)', ascending=False) # sort by date
    df3 = df2.fillna(' ') # fill NaN

    # dump results
    get_results(df3)
    
def get_results(df):
    # table header
    title_str = "| {} | {} ({}) | {} | {} ({}) | {} |".format(
        '対戦日',
        'チーム',
        'ペア',
        'スコア',
        'チーム',
        'ペア',
        'コメント'
    )
    print(title_str)
    
    title_str = "| {} | {} | {} | {} | {} |".format(
        ':---:',
        '----:',
        ':---:',
        ':----',
        ':----'
    )
    print(title_str)
    
    # format results
    md_rows = []
    for index, row in df.iterrows():
        # print("index: {}".format(index))
        # print("row: {}".format(row))
        mteam = row[1]
        oteam = row[2]
        mgames = row[3]
        ogames = row[4]
        mpair = row[5]
        opair = row[6]
        comment = row[7]
        gday = row[8]
    
        row_str = "| {} | {} ({}) | {}-{} | {} ({}) | {} |".format(
            gday,
            mteam,
            mpair,
            mgames,
            ogames,
            oteam,
            opair,
            comment 
        )
        md_rows.append(row_str)
        print(row_str)

def parse_args():
    parser = argparse.ArgumentParser(
        description = '''
        Parse raw csv for SDC 5th
        '''
    )
    parser.add_argument(
        'csv',
        help='CSV input'
    )

    args = parser.parse_args()

    if not os.path.isfile(args.csv):
        raise Exception('{} does not exist.'.format(args.csv))
    
    return args

if __name__ == '__main__':
    main()
