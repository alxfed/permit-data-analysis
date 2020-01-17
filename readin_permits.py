# -*- coding: utf-8 -*-
"""This is an example of use for Pandas machinery, the Python versions of some functions
are commented out.
"""
import socradata
import pandas as pd
# import datetime as dt
import sqlalchemy as sqlalc
import sorting
from numpy import datetime64
from io import StringIO


def main():
    dataset = 'ydr8-5enu'  # permits dataset

    # strings of parameters for request
    # start_dt = dt.datetime(year=2019, month=12, day=1, hour=0, minute=0, second=0)
    start_dt    = pd.Timestamp('2019-01-01', tz='US/Central') # much simpler, isn't it?
    # start_dt = pd.Timestamp(1546322400000, unit='ms', tz='US/Central') # HubSpot 'unix' format
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html
    start_str   = start_dt.strftime('%Y-%m-%dT%H:%M:%S')

    # end_dt = dt.datetime(year=2019, month=12, day=28, hour=0, minute=0, second=0)
    end_dt      = pd.Timestamp('2019-01-02', tz='US/Central')
    end_str     = end_dt.strftime('%Y-%m-%dT%H:%M:%S')
    # the column 'where' will be applied to
    column      = 'issue_date'

    # socrata request(s)
    response = socradata.datasets.where_a_lot_between(dataset, column, start_str, end_str)
    # exclude what can not fit into a database table anyway
    exclude_columns = ['location']  # 'xcoordinate, ycoordinate, latitude, longitude,

    result = pd.DataFrame.from_records(response, exclude=exclude_columns) # exclude works here, that's why

    # format before saving to database
    column_types = {'id': int, 'permit_': int, 'reported_cost': float,
                    # dates to numpy datetime format
                    'application_start_date': datetime64,
                    'issue_date': datetime64,
                    'processing_time': int,
                    # coordinates of location
                    'xcoordinate': float, 'ycoordinate': float,
                    'latitude': float, 'longitude': float}

    result = result.astype(column_types)

    # # without astype()
    # result['application_start_date']    = pd.to_datetime(result['application_start_date'], errors='coerce')
    # result['issue_date']                = pd.to_datetime(result['issue_date'], errors='coerce')
    # result['reported_cost']             = pd.to_numeric(result['reported_cost'], errors='coerce')
    # result['xcoordinate']               = pd.to_numeric(result['xcoordinate'])
    # result['ycoordinate']               = pd.to_numeric(result['ycoordinate'])
    # result['latitude']                  = pd.to_numeric(result['latitude'])
    # result['longitude']                 = pd.to_numeric(result['longitude'])

    permit_n = result[result['permit_'] == 100761708] # check permit #

    one = result.iloc[5]                   # check single line
    par = result.iloc[5]['issue_date']  # check the value and type

    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    result.to_sql(name=sorting.PERMITS_TABLE,
                  con=conn, if_exists='replace',
                  index=False)

    # Show summary of what came in
    print(result.head(n=3), '\n\n')
    result.info(verbose=True, memory_usage=True)
    print('\n')
    print(result.tail(n=3))
    return


if __name__ == '__main__':
    main()
    print('\n done')