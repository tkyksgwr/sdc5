import pandas as pd

df = pd.read_csv(filepath_or_buffer="5th_form_answer.csv", encoding="utf-8", sep=",")
# print(df)

# sort by date
df2 = df.sort_values('対戦日は？(省略すると本日)', ascending=False)
#print(df2)

# fill NaN
df3 = df2.fillna(' ')
#print(df3)

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
for index, row in df3.iterrows():
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