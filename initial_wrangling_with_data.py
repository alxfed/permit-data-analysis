# -*- coding: utf-8 -*-
"""Initial wrangling with downuploaded data
"""
import sqlalchemy as sqlalc
import pandas as pd
import sorting


def main():
    conn_source = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    conn_target = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)

    permits = pd.read_sql_table(table_name=sorting.PERMITS_TABLE, con=conn_source)
    # all types of permits
    types = list(permits['permit_type'].unique())

    # create separate auxiliary tables
    for type in types:
        permits_of_type = pd.DataFrame()
        permits_of_type = permits[permits['permit_type'] == type]
        permits_of_type.info()
        permits_of_type.to_sql(name=type,
                               con=conn_target, if_exists='replace',
                               index=True)        # with indexes so that it can be reassembled

        print('Saved table ', type, '  with its index\n\n')
    # permits.head(n=2)
    return


if __name__ == '__main__':
    main()
    print('main - done')