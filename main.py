import datetime

import pandas as pd

from parser import parse_data, enter_param
from database import prepare_data


def main() -> pd.DataFrame:
    df = prepare_data(5)
    # df = pd.DataFrame([[datetime.datetime(2024, 3, 2, 1, 56, 00),
    #                    datetime.datetime(2024, 3, 10, 1, 56, 00),
    #                    'БЕНЗИН (654909)', 'КУРГАН (828501)']],
    #                   columns=['start_datetime', 'operation_datetime', 'departure_station', 'operation_station'])
    df_travel = pd.DataFrame([], columns=['traveled_distance', 'traveled_days'])

    for index, row in df.iterrows():
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f'Row number in processing: {index}', sep=' | ')
        row_data: list[int] = parse_data(enter_param(row['departure_station'], row['operation_station']))

        df_row = pd.DataFrame([row_data], columns=['traveled_distance', 'traveled_days'])
        df_travel = pd.concat([df_travel, df_row], axis=0)

    df_travel = df_travel.reset_index()

    result = pd.concat([df_travel,
                        df[['start_datetime', 'operation_datetime', 'departure_station', 'operation_station']]],
                       axis=1)
    return result.loc[:, result.columns != 'index']


if __name__ == '__main__':
    pd.set_option('display.max_columns', 10)
    print('Result', main(), sep='\n', end='\n\n')
