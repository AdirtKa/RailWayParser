from sqlalchemy import create_engine
import pandas as pd


ENGINE = create_engine('postgresql://intern:V82VLVQk0u8N@DS-GIS-PostGis01.sahalin.local:5432/din_track1')


def prepare_data(rows: int = None) -> pd.DataFrame:
    df = pd.read_sql("select start_datetime, "
                     "operation_datetime, "
                     "departure_station, "
                     "operation_station, "
                     "traveled_distance "
                     "from dashboards.wagon_deployment "
                     "where departure_station not like ' (%%' and operation_station not like '%%(99%%' "
                     "order by departure_station, start_datetime, operation_datetime;", ENGINE)
    return df.loc[:rows, ['departure_station', 'operation_station', 'start_datetime', 'operation_datetime']]


if __name__ == '__main__':
    pd.set_option('display.max_columns', 10)
    print(prepare_data(3).head())
