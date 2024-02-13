import calendar
import itertools
import numpy as np
import pandas as pd

"""
Created on Sun Mar 6 23:56:45 2022
"""

class AggregationPerMonth():
    
    def __init__(self, **parameter):       
        #Data Transaksi
        data          = parameter.get('data').reset_index(drop = True)
        data['month'] = data['order_date'].dt.month
        self.data     = data
                
        #Data geografi
        datageo = parameter.get('datageo')
        if (datageo is not None):
            datageo = datageo.rename(columns = {'district' : 'city'})
            self.datageo = datageo
    
    def __getMonthNo(self, data, colMonth):
        mapmonth = dict({'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5,
                         'Jun' : 6, 'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10,
                         'Nov' : 11, 'Dec' : 12})
        data = data.reset_index()
        data['month_no'] = data[colMonth].str.slice(stop = 3).map(mapmonth)
        return data 

    def __getGeometry(self, data):
        data = data.merge(self.datageo, on = ['city', 'province'], how = 'right')
        return data
                          
    def __toList(self, value):
       if(isinstance(value, str)):
           value = value.split(',')
       else:
           value = list(value)
       return value
   
    def Sum_GMV_per_City(self):
        sum_gmv = self.data.groupby(['city', 'province', 'order_month'])\
                        .agg(sum_gmv_per_city = ('total_price', pd.Series.sum),
                             count_trx_per_city = ('order_id', pd.Series.nunique))
        sum_gmv = self.__getMonthNo(data = sum_gmv, colMonth = 'order_month')
        sum_gmv = self.__getGeometry(sum_gmv)
        sum_gmv = sum_gmv.fillna(value = {'sum_gmv_per_city' : 0, 'count_trx_per_city' : 0})\
                        .sort_values(by = ['month_no', 'province', 'city'])\
                        .reset_index(drop = True)
        return sum_gmv
    
    def Count_New_Cust_per_City(self, **parameter):
        getAttr  = list(itertools.product(parameter.get('attMonth'), parameter.get('attCity'), parameter.get('attProvince')))
        getAttr  = pd.DataFrame(getAttr, columns = ['order_month', 'city', 'province'])
        getAttr  = self.datageo.merge(getAttr, on = ['city', 'province'], how = 'inner')
        custbaru = self.data[['customer_id', 'order_month', 'city', 'province']].drop_duplicates(subset = ['customer_id'], keep = 'first', ignore_index = True)
        custbaru = custbaru.groupby(['order_month', 'city', 'province']).agg(count_new_customer = ('customer_id', pd.Series.count))
        custbaru = self.__getMonthNo(data = custbaru, colMonth = 'order_month')
        custbaru = custbaru.merge(getAttr, how = 'right', on = ['order_month', 'city', 'province'])
        custbaru = custbaru.fillna(value = {'count_new_customer' : 0}).sort_values(by = ['city', 'province', 'month_no']).reset_index(drop = True)
        custbaru = custbaru.pivot(index = 'order_month', columns = 'city', values = 'count_new_customer')
        custbaru = custbaru.reindex(parameter.get('attMonth'))
        return custbaru

    def Best_Seller_Product(self):
        best_seller = self.data.groupby(['city', 'province', 'order_month', 'product_id']).agg(best_seller_product = ('product_id', pd.Series.count))
        best_seller['best'] = best_seller.groupby(['city', 'province', 'order_month'])['best_seller_product'].transform('max')
        best_seller = best_seller[best_seller['best_seller_product'] == best_seller['best']].reset_index()
        best_seller = best_seller.drop_duplicates(subset = ['city', 'province', 'order_month'], keep = 'last', ignore_index = True)
        best_seller = best_seller.drop(columns = ['best'])
        return best_seller
