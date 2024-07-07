# import datetime
import logging

import pandas as pd

import parser
from logger import create_logger
from exceptions import UnreadbleStation, NoDataReceived
from database import prepare_data


def main() -> pd.DataFrame:
    df: pd.DataFrame = prepare_data()
    # df: pd.DataFrame = pd.DataFrame([[datetime.datetime(2024, 10, 5, 8, 9, 0),
    #                    datetime.datetime(2024, 11, 5, 6, 9, 0),
    #                    'БЕНЗИН (654909)', 'КУРГАН (828501)'],
    #                    [datetime.datetime(2024, 11, 6, 7, 9, 0),
    #                     datetime.datetime(2024, 11, 20, 0, 0, 0),
    #                     'БЕНЗИН (654909)', 'ХОЛБОН (948050)']
    #                    ],
    #                   columns=['start_datetime', 'operation_datetime', 'departure_station', 'operation_station'])
    df_travel: pd.DataFrame = pd.DataFrame([], columns=['traveled_distance', 'traveled_days'])

    logger: logging.Logger = create_logger()
    for index, row in df.iterrows():
        logger.info(f'Row number in processing: {index}\n'
                    f'\tdeparture_station {row['departure_station']}\n'
                    f'\toperation_station {row['operation_station']}')

        row_data: list[int] = [0, 0]
        try:
            row_data: list[int] = parser.enter_param_rzd_cargo(row['departure_station'],
                                                               row['operation_station'])
        except (UnreadbleStation, NoDataReceived) as ex:
            logger.warning(ex.message)

        df_row: pd.DataFrame = pd.DataFrame([row_data], columns=['traveled_distance', 'traveled_days'])
        df_travel: pd.DataFrame = pd.concat([df_travel, df_row], axis=0)

    df_travel: pd.DataFrame = df_travel.reset_index()

    result: pd.DataFrame = pd.concat([df_travel,
                                            df[['start_datetime',
                                                'operation_datetime',
                                                'departure_station',
                                                'operation_station']]],
                                           axis=1)
    return result.loc[:, result.columns != 'index']


if __name__ == '__main__':
    pd.set_option('display.max_columns', 10)
    print('Result', main(), sep='\n', end='\n\n')
