import datetime

import pandas as pd

from parser import parse_data, enter_param
from database import prepare_data


def main() -> pd.DataFrame:
    # df = prepare_data()
    df = pd.DataFrame([[datetime.datetime(2024, 3, 2, 1, 56, 0), 'БЕНЗИН (654909)', 'КОРМИЛОВКА (832704)'],
                       [datetime.datetime(2024, 6, 7, 10, 20, 50), 'БЕНЗИН (654909)', 'КУРГАН (828501)']],
                      columns=['start_datetime', 'departure_station', 'operation_station'])
    df_travel = pd.DataFrame([], columns=['traveled_distance', 'operation_datetime'])

    for index, row in df.iterrows():
        row_data = parse_data(enter_param(row['departure_station'], row['operation_station']))
        # calculate potential arrived time(operation_datetime)
        row_data[1] = row['start_datetime'].replace(day=row['start_datetime'].day + row_data[1])

        df_row = pd.DataFrame([row_data], columns=['traveled_distance', 'operation_datetime'])
        df_travel = pd.concat([df_travel, df_row], axis=0)

    df_travel = df_travel.reset_index()

    result = pd.concat([df_travel,
                        df[['start_datetime', 'departure_station', 'operation_station']]],
                       axis=1)
    return result.loc[:, result.columns != 'index']


if __name__ == '__main__':
    pd.set_option('display.max_columns', 10)
    print(main())
