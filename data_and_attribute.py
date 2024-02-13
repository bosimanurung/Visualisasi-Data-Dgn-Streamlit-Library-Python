import os
os.path.dirname(os.path.realpath('__file__'))

import calendar
import numpy as np
import pandas as pd
import geopandas as gpd

"""
Created on Sat Mar 5 23:49:54 2022
"""

class Data():
    
    def __init__(self):
        #Proses ekstrak data
        self.dataSourceRaw   = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/retail_raw_reduced_data_quality.csv')
        self.dataGeo         = self.geoMaps()
        self.dataSourceClean = self.__TransformAndCleansing()
        
    def __TransformAndCleansing(self):
        data    = self.dataSourceRaw
        datageo = self.dataGeo[['province', 'district']]
        datageo = datageo.rename(columns = {'province' : 'provinsi'})
        data    = data.merge(datageo, how = 'left', left_on = 'city', right_on = 'district')
        
        #Proses transformasi dan cleansing
        data = data.dropna(subset = ['order_id'])
        data[['order_id', 'customer_id']] = data[['order_id', 'customer_id']].astype('str')
        data['province']   = np.where(data['province'].isnull(), data['provinsi'], data['province'])
        data['city']       = np.where(data['city'].isnull(), 'N/A - ' + data['province'], data['city'])
        data['order_date'] = pd.to_datetime(data['order_date'], format = '%d/%m/%Y')
        data = data.drop(columns = ['provinsi', 'district'])

        #Penambahan kolom
        data['total_price'] = data['quantity'] * data['item_price']
        data.insert(loc = 2, column = 'order_year' , value = data['order_date'].dt.year)
        data.insert(loc = 2, column = 'order_month', value = data['order_date'].dt.month_name())
        return data

    def __toList(self, value):
       if(isinstance(value, str)):
           value = value.split(',')
       else:
           value = list(value)
       return value
    
    def __filterCol(self, **parameter):
        data = parameter.get('data')
        rec  = parameter.get('rec')
        if (rec is not None):
            col  = parameter.get('col')
            try :
                record = self.__toList(rec)
                data   = data[data[col].isin(record)]
            except:
                 pass
        return data.reset_index(drop = True)
        
    def getDataRetail(self, **parameter):
        #Assignment ke variabel lain
        data    = self.dataSourceClean
        
        #Filter data berdasarkan kota atau provinsi
        data = self.__filterCol(data = data, col = 'city', rec = parameter.get('city'))
        data = self.__filterCol(data = data, col = 'province', rec = parameter.get('province'))
        data = self.__filterCol(data = data, col = 'order_month', rec = parameter.get('month'))
        
        return data 
    
    def geoMaps(self, **parameter):
        os.path.dirname(os.path.realpath('__file__'))
        datageo = gpd.read_file('gadm36_IDN_2.shp')
        datageo = datageo.rename(columns = {'NAME_1' : 'province', 'NAME_2' : 'district'})
        datageo = datageo[['province', 'district', 'geometry']]
        datageo = datageo[~datageo['district'].isin(['Kepulauan Seribu', 'Waduk Kedungombo'])]

        for m, n in {'Kota Yogyakarta' : 'Yogyakarta', 'Jakarta Raya' : 'DKI Jakarta'}.items():
            datageo['province'] = datageo['province'].str.replace(m, n)
            datageo['district'] = datageo['district'].str.replace(m, n)

        datageo = self.__filterCol(data = datageo, col = 'province', rec = parameter.get('province'))
        return datageo

    def __getAttr(func):
        def filterAttribute(self, **parameter):
            #Untuk attribute city --> filter berdasarkan provinsi dipilih
            province = parameter.get('province')
            if(province is not None):
                province = self.__toList(province)
                data     = self.dataSourceClean[self.dataSourceClean['province'].isin(province)]
            else:
                data = self.dataSourceClean
                
            #Untuk attribute lain
            data = data[func(self)] if isinstance(func(self), str) else data[func(self)[0]]
            data = data.dropna().drop_duplicates()
            data = data.sort_values(ignore_index = True).to_list()
            if(func(self) == 'order_month'): 
                data = sorted(data, key = list(calendar.month_name).index)
            return data
        return filterAttribute
    
    @__getAttr
    def getAttrProvince(self):
        return('province')
    
    @__getAttr
    def getAttrCity(self, province = None):
        return('city', province)
    
    @__getAttr
    def getAttrMonth(self):
        return('order_month')
    
    @__getAttr
    def getAttrYear(self):
        return('order_year')
