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
    conn_source = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)
    conn_target = sqlalc.create_engine(sorting.INTERM_DATABASE_URI)

    permits = pd.read_sql_table(table_name='PERMIT - EASY PERMIT PROCESS', con=conn_source)

    # all_columns = permits.columns.values
    # useful_columns_for_plotting = ['id', 'permit_', 'permit_type', 'review_type',
    #                                'application_start_date', 'issue_date', 'processing_time',
    #                                'street_number', 'street_direction', 'street_name', 'suffix',
    #                                'work_description', 'reported_cost',
    #                                'xcoordinate', 'ycoordinate', 'latitude', 'longitude']
    #
    # permits_for_plotting = permits.loc[:,useful_columns_for_plotting] # this is a subsetted copy
    #
    reported_costs = permits.loc[:, ['reported_cost']]
    # bins = numpy.logspace(start=1, stop=8, num=1, endpoint=True)
    # reported_costs.plot.hist(bins=bins)
    #
    extra_big_removed = reported_costs[reported_costs['reported_cost'] < 50000]
    extra_big_removed.plot.hist(bins=10, histtype='step', figsize=(8, 8))
    plt.show()

    bins = numpy.logspace(start=1, stop=8, num=1, endpoint=True)
    reported_costs.plot.hist(by='permit_type', bins=bins) # , column='reported_cost'


    reported_costs.to_sql(name='reported_costs',
                           con=conn_target, if_exists='replace',
                           index=False)        # with indexes it can be reassembled
    return


if __name__ == '__main__':
    main()
    print('main - done')