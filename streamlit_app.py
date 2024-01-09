import os
import numpy as np
import pandas as pd
import streamlit as st
#bsadded 11Des22
import matplotlib.pyplot as plt
import matplotlib.colors as pltc
from PIL import Image
#import geopandas as gpd
import data_and_attribute
import aggregation as agg
import visualization as viz
from datetime import datetime

st.set_page_config(layout="wide")
os.path.dirname(os.path.realpath('__file__'))

#Set Atribut Visualisasi
Extract           = data_and_attribute.Data()
attributeYears    = Extract.getAttrYear()
attributeMonth    = Extract.getAttrMonth()
attributeProvince = Extract.getAttrProvince()

##### Seleksi Data (Side Bar) #####
#st.sidebar.markdown("**Seleksi Data yang akan di Analisa:** 👇")
st.sidebar.markdown("**Seleksi Data yang akan di Analisa:**")

year     = st.sidebar.selectbox('Pilih Tahun', attributeYears)
month    = st.sidebar.selectbox('Pilih Bulan', attributeMonth).split()
province = st.sidebar.multiselect('Pilih Provinsi', ['All'] + attributeProvince, 'DKI Jakarta')

if('All' in province):
    province = attributeProvince
    
attributeCities = Extract.getAttrCity(province = province)

for i in range(3):
    st.sidebar.text('')
    
st.sidebar.text('Powered by: ')
#image = Image.open('DQLab.png')
image = Image.open('BosiManurungSoftwareDevelopment3.png')
st.sidebar.image(image)

#dataretail = pd.read_csv('https://dataset.dqlab.id/retail_raw_reduced.csv')
#dataretail_strukturdata = pd.read_excel('c:/bsapp/streamlit/retail_raw_reduced_bsstrukturdata.xlsx')

#dataretail['total_revenue'] = dataretail['quantity'] + dataretail['item_price']

#print(dataretail)     
#print(datasampah.columns)                
#print(datasampah.info())'''

#membuat dashboard berdasarkan provinsi
#attributeProvince = dataretail['province'].unique().tolist()
#print(attributeProvince)

#Ambil tabel transaksi
datatrxfull = Extract.getDataRetail(province = province)
datatrxmth  = datatrxfull.loc[datatrxfull['order_month'].isin(month)].reset_index(drop = True)
datageo     = Extract.geoMaps(province = province)

#Aggregasi
sum_gmv_per_city = agg.AggregationPerMonth(data = datatrxmth,  datageo = datageo).Sum_GMV_per_City()
                            
best_seller_prod = agg.AggregationPerMonth(data = datatrxmth).Best_Seller_Product()
                            
#Data aggregasi ditampilkan
sum_revenue = pd.DataFrame(sum_gmv_per_city[['city', 'province', 'sum_gmv_per_city', 'count_trx_per_city']])
sum_revenue = sum_revenue.loc[sum_revenue['count_trx_per_city'] > 0].dropna()\
                    .sort_values(by = ['sum_gmv_per_city', 'count_trx_per_city'], ascending = False)\
                    .reset_index(drop = True)  

mapCityAndProduct = ''
for index in range(best_seller_prod.shape[0]):
    mapCityAndProduct += 'best seller product di ' + best_seller_prod['city'][index] + ' (' +\
                            best_seller_prod['product_id'][index] + '), '
mapCityAndProduct = mapCityAndProduct.rstrip(', ')

#Visualisasi

fig_geo, ax_geo       = viz.Visualization(sum_gmv_per_city).geoGraph(colValues = 'sum_gmv_per_city',
                                                                      annotate = 'city')

fig_bubble, ax_bubble = viz.Visualization(best_seller_prod).bubbleGraph(annotate = ['city', 'product_id'], 
                                                                        area = 'best_seller_product',
                                                                        figsize = (15, 10))

#bikin dashboard
#baris 1 - Title & Deskripsi
#variabel bebas utk garis tepi kiri, isi, garis tepi kanan :
#row1_spacer1, row1_1, row1_spacer2 = st.columns((0.02, 3, 0.02)) 
row1_spacer1, row1_1, row1_spacer2 = st.columns((0.02, 3, 0.09)) 
with row1_1:
    st.markdown("<p style='color:blue; font-style:strong; font-family:arial; font-size:300%'>DASHBOARD :</p>", unsafe_allow_html=True)
    #st.title("DASHBOARD :")
    st.markdown("<p style='color:blue; font-family:arial; font-style:strong; font-size:250%'>KEY PERFORMANCE \
                INDICATOR (KPI)</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:blue; font-family:arial; font-style:strong; font-size:250%'>OF BM-MARKETPLACE</p>", unsafe_allow_html=True)    
    #st.title("DQ-MARKETPLACE'S KEY PERFORMANCE INDICATOR")

    #st.subheader('Streamlit App by https://www.linkedin.com/in/bosimanurung')
    st.markdown("<p style='font-size:200%'><strong>Streamlit App by \
                <a href='https://www.linkedin.com/in/bosimanurung/'>Bosi Manurung</a></strong></p>", unsafe_allow_html=True)
    #<p id="top"><a href="http://www.google.com/">Click Here To Go Google.com</a></p>
    
    st.markdown("<p style='text-align:justify;'><strong><span style='font-size:105%'>\
                Key Performance Indicator (KPI)</span></strong> adalah alat ukur kuantitatif yang \
                menggambarkan efektivitas perusahaan. Tidak hanya soal seberapa \
                besarnya angka, namun juga apakah performa perusahaan sudah sesuai \
                dengan tujuan bisnis yang diharapkan sebelumnya. <strong><span style='font-size:105%'> \
                BM-MarketPlace</span></strong> adalah sebuah \
                perusahaan yang bergerak di bidang retail (bisnis yang melibatkan \
                penjualan barang atau jasa kepada konsumen dalam jumlah satuan/eceran) \
                yang menetapkan tiga kriteria KPI-nya yakni Total Revenue, New Customer Growth \
                dan Best Seller Product (dalam jangka waktu bulan tertentu). Dengan mengukur \
                ketiga KPI tersebut diharapkan perusahaan mampu mengevaluasi performa \
                bisnis dan merencanakan strategi berikutnya.</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align:justify;'>Data sumber adalah file retail_raw_reduced.csv yang berasal dari API dataset <a href='https://dataset.dqlab.id'>dqlab.</a> Bila ingin mendownload file tersebut, \
                silakan klik <a href='https://dataset.dqlab.id/retail_raw_reduced.csv'>link</a> ini.</p>", unsafe_allow_html=True)     

##### Tampilkan Data #####
row2_spacer1, row2_1, row2_spacer1 = st.columns((.2, 7.1, .2))
with row2_1:
    st.subheader("Data Transaksi {} {} pada Provinsi {}".format(" ".join(month), year, " - ".join(province)))
    st.markdown("Data yang ditampilkan berikut telah melalui tahap proses transformasi (penambahan kolom, penyesuaian tipe data, dsb) dan proses cleansing.")

row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
with row3_1:
    st.markdown("")
    #see_data = st.expander('Klik tautan berikut untuk melihat detail data yang digunakan 👉')
    #with see_data:
    #    showdata = datatrxmth.drop(columns = ['order_month', 'order_year'])
    #    showdata = showdata.style.format({"quantity": "{:.0f}", "item_price": "Rp. {:,.2f}", "total_price": "Rp. {:,.2f}"})
    #    st.dataframe(data = showdata)

    showdata = datatrxmth.drop(columns = ['order_month', 'order_year'])
    #bseditted13Des22 showdata = showdata.style.format({"quantity": "{:.0f}", "item_price": "Rp. {:,.2f}", "total_price": "Rp. {:,.2f}"})
    showdata = showdata.style.format({"order_date": "{:%d/%m/%Y}", "quantity": "{:.0f}", "item_price": "Rp. {:,.2f}", "total_price": "Rp. {:,.2f}"})
    
    st.dataframe(showdata)    
        
#baris 2 - Tampilkan datanya (bikin variabel baru)
#row2_spacer1, row2_1, row2_spacer2 = st.columns((0.02, 3, 0.02))
#with row2_1:
#    st.subheader('Data yang digunakan') 
#    st.dataframe(dataretailprovinsi)    
    #st.markdown("Deskripsi kolom dari tabel tersebut adalah:", unsafe_allow_html=True)  
    #st.markdown("1. order_id    : ID dari order atau transaksi. Satu ID bisa terdiri dari beberapa produk, tapi hanya untuk 1 customer.", unsafe_allow_html=True)  
    
    #st.markdown("Deskripsi kolom dari tabel tersebut adalah:")
    #st.dataframe(dataretail_strukturdata.style.hide_index())     
    #st.write("order_id    : ID dari order/transaksi. Satu ID atau order/transaksi bisa terdiri dari beberapa produk yang dipesan. ", 
             #"order_date  : Tanggal order/transaksi.")


#baris 3 - Tampilkan Keterangan datanya (bikin variabel baru)
#style = dataretail_strukturdata.style.hide_index()
#dataretail_strukturdata.set_index('column', inplace=True)
row3_spacer1, row3_1, row3_spacer2 = st.columns((0.02, 3, 0.02))
with row3_1:
    st.markdown("Deskripsi kolom dari tabel tersebut adalah:")    
    #st.dataframe(dataretail_strukturdata.style.hide_index()) 
    
    #st.write(style.to_html(), unsafe_allow_html=True)
    #st.dataframe(dataretail_strukturdata) 
    
    kolomdesc = '\n1.  order_id\t: ID dari order atau transaksi, 1 transaksi bisa terdiri dari beberapa produk, tetapi hanya dilakukan oleh 1 customer\
                 \n2.  order_date\t: tanggal terjadinya transaksi\
                 \n3.  customer_id\t: ID dari pembeli; bisa jadi dalam satu hari, 1 customer melakukan transaksi beberapa kali\
                 \n4.  city\t: kota tempat toko terjadinya transaksi\
                 \n5.  province\t: provinsi (berdasarkan city)\
                 \n6.  product_id\t: ID dari suatu product yang dibeli\
                 \n7.  brand\t: brand/merk dari product. Suatu product yang sama pasti memiliki brand yang sama\
                 \n8.  quantity\t: Kuantitas/banyaknya product yang dibeli\
                 \n9.  item_price\t: Harga dari 1 product (dalam Rupiah). Suatu product yang sama, bisa jadi memiliki harga yang berbeda saat dibeli\
                 \n10. total_price\t: Hasil kali barang dibeli (quantity) dengan harga barang (item_price)'
    st.text(kolomdesc)    

    
##### Tampilkan GeoGraph #####
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.header("Total Revenue {} {} Per Kota pada Provinsi {}".format(" ".join(month), year, " - ".join(province)))
    st.pyplot(fig = fig_geo)
                  
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3 = st.columns((.2, 7.1, .2, 7.1, .2))
with row5_1:
    stdrevenue = sum_revenue['sum_gmv_per_city'].mean()
    stdrevenue = st.number_input('Standart Total Revenue : ', stdrevenue)
    condition = [sum_revenue['sum_gmv_per_city'] >= stdrevenue]
    sum_revenue['category'] = np.select(condition, ['above standard'], ['below standard'])
    st.dataframe(sum_revenue.style.format({"sum_gmv_per_city" : "{:.2f}", "count_trx_per_city": "{:.0f}"})) 
with row5_2:
    st.text('')
    st.markdown('<div style="text-align: justify;">Pada bulan {} {} di Provinsi {} \
                diperoleh pendapatan total sebesar <strong>{:,.2f}</strong>.\
                 Total pendapatan terbesar terjadi di <strong>{}</strong> sebesar \
                <strong>{:,.2f}</strong>\
                 dengan banyak transaksi yang terjadi sebanyak {:.0f} kali.<break></div>'\
                    .format(" ".join(month), 
                            year, " - ".join(province),
                                sum_revenue['sum_gmv_per_city'].sum(),
                            sum_revenue['city'][0],
                            sum_revenue['sum_gmv_per_city'][0],
                            sum_revenue['count_trx_per_city'][0]
                            ), unsafe_allow_html=True)
        
    if(sum_revenue.shape[0] > 1):
        st.text('')
        st.markdown('<div style="text-align: justify;">Sebaliknya, total pendapatan terkecil terjadi di <strong>{}</strong> sebesar <strong>{:,.2f}</strong>\
                     dengan banyak transaksi yang terjadi sebanyak {:.0f} kali.</div>'\
                         .format(sum_revenue['city'][sum_revenue.shape[0]-1],
                                 sum_revenue['sum_gmv_per_city'][sum_revenue.shape[0]-1],
                                 sum_revenue['count_trx_per_city'][sum_revenue.shape[0]-1]), unsafe_allow_html=True)
st.markdown('')

row5a_spacer1, row5a_1, row5a_spacer2 = st.columns((.2, 7.1, .2))
with row5a_1:
    st.markdown('<div style="text-align: justify;">**nb** : *Standar Total Revenue awal yang diinisialisasi adalah rata-rata dari total revenue tiap kota pada provinsi {}\
                 yakni sebesar {}. Anda dapat menaikkan atau menurunkan standar dengan menginputkan nilai pada tempat yang disediakan*</div>'\
                 .format(" - ".join(province), stdrevenue), unsafe_allow_html=True)    


##### Tampilkan BubbleChart #####
row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.header("Produk Paling Laris {} {} Per Kota pada Provinsi {}".format(" ".join(month), year, " - ".join(province)))

row7_spacer1, row7_1, row7_spacer2 = st.columns((1.5, 7.1, 1.5))
try:    
    with row7_1:
        st.pyplot(fig = fig_bubble)

    row8_spacer1, row8_1, row8_spacer2 = st.columns((.2, 7.1, .2))
    with row8_1:
        st.markdown('Pada bulan {} {} di Provinsi {} diperoleh beberapa produk paling laris terjual (best seller product)\
                    diantaranya {})'\
                            .format(" ".join(month), year, " - ".join(province), mapCityAndProduct))
        st.markdown('**nb** : *Produk dikategorikan sebagai produk yang best seller didasarkan pada perhitungan banyaknya transaksi\
                     terkait produk tersebut bukan berdasarkan kuantitas produk tersebut terjual (jumlah kuantitas produk terjual*')
except :
    with row7_1:
        st.error('Tidak ada data yang ditampilkan')


#row9_spacer1, row9_1, row9_spacer2 = st.columns((.2, 6.1, .2))
row9_spacer1, row9_1, row9_spacer2 = st.columns((.2, 6.1, .2))
with row9_1:
    #st.header("Pertumbuhan New Customer {} - {} {} Per Kota pada Provinsi {}"\
                  #.format(attributeMonth[0], attributeMonth[len(attributeMonth)-1], year, " - ".join(province)))
    st.header("Pertumbuhan New Customer {} - {} {} Pada Provinsi {}"\
                  .format(attributeMonth[0], attributeMonth[len(attributeMonth)-1], year, " - ".join(province)))                        
    attributeCities = [i for i in attributeCities if 'N/A' not in i]
    options         = st.multiselect('Pilih Kota / Kabupaten', attributeCities, attributeCities)
    new_cust_growth = agg.AggregationPerMonth(data = datatrxfull, datageo = datageo)\
                                .Count_New_Cust_per_City(attMonth = attributeMonth,
                                                         attCity = options, 
                                                         attProvince = province)
    #fig_line, ax_line = viz.Visualization(new_cust_growth).lineGraph(figsize = (15, 10))
    fig_line, ax_line = viz.Visualization(new_cust_growth).lineGraph(figsize = (11, 6))
    st.pyplot(fig = fig_line)
    
    perc_growth = new_cust_growth.pct_change().fillna(0).round(4) * 100
    see_data = st.expander('Klik tautan berikut untuk melihat detail data presentase kenaikkan atau penuruan new cust yang digunakan 👉')
    with see_data:
        st.dataframe(data = perc_growth.applymap('{:.2f}%'.format))
    
mean_of_perc = perc_growth.mean().sort_values(ascending = False)\
                        .reset_index().rename(columns = {0 : 'rataan_pertumbuhan', 'city' : 'kota'})
mean_of_perc['rataan_pertumbuhan'] = mean_of_perc['rataan_pertumbuhan']
mean_of_perc['ispositive?'] = np.select([mean_of_perc['rataan_pertumbuhan'] > 0], [True], [False])


row10_spacer1, row10_1, row10_spacer2, row10_2, row10_spacer3 = st.columns((.2, 7.1, .2, 7.1, .2))   
with row10_1:         
    st.markdown('**Rata - rata presentase pertumbuhan new customer**')
    st.dataframe(data = mean_of_perc.drop(columns = 'ispositive?').style.format({"rataan_pertumbuhan": "{:.2f}%"}))
with row10_2:
    for i in range(2):
        st.text('')
    st.markdown('Rata-rata pertumbuhan pelanggan baru (*new customer*) tiap kota atau kabupaten pada provinsi {}\
                disajikan pada tabel disamping. Dengan rataan pertumbuhan paling baik terjadi di **{}**\
                sebesar **{:.2f}%** dan rataan pertumbuhan pelanggan baru paling rendah terjadi di **{}**\
                sebesar **{:.2f}%**'\
                    .format(" - ".join(province),
                        mean_of_perc['kota'][0],
                        mean_of_perc['rataan_pertumbuhan'][0],
                        mean_of_perc['kota'][mean_of_perc.shape[0]-1],
                        mean_of_perc['rataan_pertumbuhan'][mean_of_perc.shape[0]-1]
                    )
                )

try:
    belowstd = sum_revenue[sum_revenue['category'] == 'below standard'].reset_index(drop = True)
    if(belowstd.shape[0] > 0):
        citybelowstd = ", ".join(belowstd['city'].to_list())
except:
    pass
row11_spacer1, row11_1, row11_spacer2 = st.columns((.2, 7.1, .2))
with row11_1:
    st.header('Summary')
    st.markdown('<div style="text-align: justify;">Pada hasil analisa diperoleh beberapa fakta bahwa terdapat beberapa kota atau kabupaten pada provinsi\
                {} yang menghasilkan total revenue dibawah standar yang ditetapkan sebesar **{:.0f}** yakni kota / kabupaten {}. Sehingga perlu\
                dilakukan evaluasi lebih lanjut dari sisi marketing (*campaign*), kualitas produk, *customer experience* dan sebagainya\
                agar kedepannya perusahaan dapat meningkatkan penjualan di tempat tersebut. Dapat juga memberikan tawaran yang menarik atau promosi\
                pada beberapa produk yang best seller seperti {}. Karena produk yang disebutkan merupakan produk yang paling diminati di masing-masing kota/kab tersebut.\
                </div>'.format(" - ".join(province), stdrevenue, citybelowstd, mapCityAndProduct), unsafe_allow_html=True)
    
    st.markdown('<div style="text-align: justify;">Pertumbuhan *new customer* yang paling baik terjadi di kota/kab **{}** sebesar **{:.2f}%** sehingga kota/kab tersebut bisa menjadi pacuan atau tolak ukur \
                 kota atau kabupaten yang lainnya agar perusahaan dapat menggaet lebih banyak lagi *new customer*. Beberapa cara yang bisa dilakukan \
                 untuk menggaet *new customer* dan mempertahankannya adalah buat penawaran secara personal berdasarkan data, maksimalkan *campaign* di medsos dan dunia nyata,\
                 cek laporan produk, buat promosi yang menarik dan sebagainya</div>'
                .format(mean_of_perc['kota'][0], mean_of_perc['rataan_pertumbuhan'][0]), unsafe_allow_html=True)
