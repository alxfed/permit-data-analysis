# -*- coding: utf-8 -*-
"""...
"""
import sqlalchemy as sqlalc
import pandas as pd
import sorting


def main():
    conn_source = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    conn_target = sqlalc.create_engine(sorting.PREP_DATABASE_URI)

    permits = pd.read_sql_table(table_name=sorting.PERMITS_TABLE, con=conn_source)
    # all types of permits
    types = list(permits['permit_type'].unique())  # unique returns a numpy Array

    permits_categorised = permits.copy()
    convert_to_categories = ['permit_type', 'review_type']
    permits_categorised[convert_to_categories] = permits_categorised[convert_to_categories].astype('category')

    permits_categorised.info(verbose=True)
    # one = permits_categorised.iloc[5]  # check single line of the table (debug)
    # par = type(permits_categorised.iloc[5]['permit_type']) # check the value and type (debug)
    return


if __name__ == '__main__':
    main()
    print('main - done')