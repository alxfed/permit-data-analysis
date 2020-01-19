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
    permits_categorised[['permit_type', 'review_type']] = permits_categorised[['permit_type', 'review_type']].astype('category')

    permits_categorised.to_sql(name=sorting.constants.PERMITS_CATEGORISED,
                        con=conn_target, if_exists='replace',
                        index=False)

    print('Saved categorised permits to ', sorting.PREP_DATABASE_URI, '\t', sorting.constants.PERMITS_CATEGORISED, '\n')
    return


if __name__ == '__main__':
    main()
    print('main - done')