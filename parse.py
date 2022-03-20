#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import logging
import os
import pandas as pd
import sys

args = []

def main():
    global args
    args = parse_args()

    # logging
    if args.Debug:
        logging.basicConfig(level=logging.DEBUG)

    df = pd.read_csv(filepath_or_buffer=args.csv, encoding="utf-8", sep=",")
    # print(df)
    
    df2 = df.sort_values('対戦日は？(省略すると本日)', ascending=False) # sort by date
    df3 = df2.fillna(' ') # fill NaN

    # dump team results
    if args.team:
        get_team_results(df3)

    # dump results
    get_results(df3)

def get_teams():

    teams = []
    teams.append('チーム徳川家康')
    teams.append('東京シティBoys')
    teams.append('TUBE')
    teams.append('お上品関西軍団')
    teams.append('チーム桃太郎')
    teams.append('チームNAHANAHA')
    logging.debug(teams)

    return teams

def get_team_results(df):

    teams = get_teams()
    sys.exit()

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
        Parse raw csv for SDC 5th and output results
        '''
    )
    parser.add_argument(
        'csv',
        help='CSV input'
    )
    parser.add_argument(
        '-t', '--team',
        action='store_true',
        help='Output team results'
    )
    parser.add_argument(
        '-D', '--Debug',
        action='store_true',
        help='Debug mode'
    )

    args = parser.parse_args()

    if not os.path.isfile(args.csv):
        raise Exception('{} does not exist.'.format(args.csv))
    
    return args

if __name__ == '__main__':
    main()
