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
    logging.debug(df)
    
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

    # Header
    win_loss_str = "| {} | {} | {} | {} | {} | {} | {} | {} | {}|".format(
        '---',
        teams[0],
        teams[1],
        teams[2],
        teams[3],
        teams[4],
        teams[5],
        'チーム勝敗',
        'チーム順位'
    )
    print(win_loss_str)
    win_loss_str = "| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
        '----:',
        ':---:',
        ':---:',
        ':---:',
        ':---:',
        ':---:',
        ':---:',
        ':---:',
        ':---:',
    )
    print(win_loss_str)

    for team in teams:
        logging.debug(team)

        win_loss = []
        team_win = 0
        team_loss = 0
        for oteam in teams:
            if team == oteam:
                win_loss.append('---')
                continue

            # Extract wins and losses
            # df_win = df[(df['あなたのチームは？'] == team) & (df['対戦相手は？'] == oteam)]
            # df_win = df_win[df_win['ダブルスの結果 [あなた]'] == 6]
            df_win = df[(df['あなたのチームは？'] == team) & (df['対戦相手は？'] == oteam) & (df['ダブルスの結果 [あなた]'] == 6)]
            logging.debug(df_win)
            num_win = len(df_win)
            logging.debug("num_win: {}".format(num_win))
            num_loss = len(df[(df['あなたのチームは？'] == team) & (df['対戦相手は？'] == oteam) & (df['ダブルスの結果 [対戦相手]'] == 6)])
            num_win_alt = len(df[(df['あなたのチームは？'] == oteam) & (df['対戦相手は？'] == team) & (df['ダブルスの結果 [対戦相手]'] == 6)])
            num_loss_alt = len(df[(df['あなたのチームは？'] == oteam) & (df['対戦相手は？'] == team) & (df['ダブルスの結果 [あなた]'] == 6)])
            num_win = num_win + num_win_alt
            num_loss = num_loss + num_loss_alt

            win_loss_str = "{}-{}".format(num_win, num_loss)

            # count games if even
            if num_win == num_loss:
                df_games = df[(df['あなたのチームは？'] == team) & (df['対戦相手は？'] == oteam)].sum()
                num_games = df_games['ダブルスの結果 [あなた]']
                num_ogames = df_games['ダブルスの結果 [対戦相手]']
                logging.debug('num_games: {}'.format(num_games))

                df_games_alt = df[(df['あなたのチームは？'] == oteam) & (df['対戦相手は？'] == team)].sum()
                num_games_alt = df_games_alt['ダブルスの結果 [対戦相手]']
                num_ogames_alt = df_games_alt['ダブルスの結果 [あなた]']
                logging.debug('num_games_alt: {}'.format(num_games_alt))

                num_games = num_games + num_games_alt
                num_ogames = num_ogames + num_ogames_alt

                win_loss_str = "{} ({}-{})".format(win_loss_str, int(num_games), int(num_ogames))
                
            win_loss.append(win_loss_str)

            # calc team win loss
            if (num_win + num_loss) > 2:
                if num_win > num_loss:
                    team_win += 1
                if num_win < num_loss:
                    team_loss += 1
            
            # case: 2-2
            if (num_win == 2) and (num_loss == 2):
                if num_games > num_ogames:
                    team_win +=1
                if num_games < num_ogames:
                    team_loss += 1

        team_win_loss = "{}-{}".format(team_win, team_loss)
        team_rank = '--'

        #logging.debug(df[df['あなたのチームは？'] == team])
        win_loss_str = "| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            team,
            win_loss[0],
            win_loss[1],
            win_loss[2],
            win_loss[3],
            win_loss[4],
            win_loss[5],
            team_win_loss,
            team_rank
        )
        print(win_loss_str)

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
