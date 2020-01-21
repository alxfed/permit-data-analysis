# -*- coding: utf-8 -*-
"""Initial wrangling with downuploaded data
"""
import sqlalchemy as sqlalc
import pandas as pd
import sorting
import matplotlib.pyplot as plt
import numpy
# import seaborn.a as sns
#
# sns.set() #rescue matplotlib's styles from the early '90s
#


def main():
    conn_source = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    conn_target = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)

    permits = pd.read_sql_table(table_name=sorting.PERMITS_TABLE, con=conn_source)
    # all types of permits
    types_list = list(permits['permit_type'].unique())  # unique returns a numpy Array
    permit_types = pd.DataFrame(types_list, columns=['permit_type'])
    permit_types.to_sql(name=sorting.constants.PERMIT_TYPES_TABLE,
                        con=conn_target, if_exists='replace',
                        index=False)
    print('Saved permit types to ', sorting.constants.PERMIT_TYPES_TABLE, '\n\n')

    # all_columns = permits.columns.values
    useful_columns_for_plotting = ['id', 'permit_', 'permit_type', 'review_type',
                                   'application_start_date', 'issue_date', 'processing_time',
                                   'street_number', 'street_direction', 'street_name', 'suffix',
                                   'work_description', 'reported_cost',
                                   'xcoordinate', 'ycoordinate', 'latitude', 'longitude']

    permits_for_plotting = permits.loc[:,useful_columns_for_plotting] # this is a subsetted copy

    reported_costs = permits.loc[:, ['permit_type', 'reported_cost']]
    reported_costs.hist(by='permit_type', column='reported_cost')
    plt.show()

    bins = numpy.logspace(start=1, stop=9, num=1, endpoint=True)
    reported_costs.plot.hist(by='permit_type', bins=bins) # , column='reported_cost'

    plt.show()
    print('Are you ok?')
    # create/save separate auxiliary table for each type
    for type in types_list:
        permits_of_type = pd.DataFrame()
        permits_of_type = permits[permits['permit_type'] == type]
        permits_of_type.info() # print out a summary of what will be saved
        permits_of_type.to_sql(name=type,
                               con=conn_target, if_exists='replace',
                               index=False)        # with indexes it can be reassembled

        print('Saved table ', type, '  with its index\n\n')
    else:
        print('Done saving to:  ', sorting.constants.TARGET_DATABASE_URI)
    # permits.head(n=2)
    return


if __name__ == '__main__':
    main()
    print('main - done')