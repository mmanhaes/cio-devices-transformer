from sklearn import preprocessing
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from datetime import datetime
import numpy as np

class CustomTransformerV2(BaseEstimator,TransformerMixin):
    
    def getDeviceId(self,entry):
               
        entry = str(entry)

        return entry.split('-')[0].strip()
    
    def getVendor(self,entry):

        entry = str(entry)

        return entry.split(' ')[0]
    
    
    def handlingMemoryData(self,entry):
        if isinstance(entry, int):

            return entry

        else:

            entry = str(entry)

            entry = entry.replace('GB','')

            return int(entry)
        
        
    def handlingDates(self,entry):
        if (type(entry) is int):

            return entry

        else:

            entry = str(entry)
            #ValueError: time data '2017-04-06 00:00:00' does not match format '%m/%d/%Y %I:%M:%S %p'
            #ValueError: time data '4/6/2017 0:00' does not match format '%Y-%m-%d %H:%M:%S'
            date_format = "%Y-%m-%d %H:%M:%S" 
            try:
                a = datetime.strptime(entry, date_format)
            except:
                date_format = "%m/%d/%Y %H:%M"
                a = datetime.strptime(entry, date_format)

            b = datetime.today()
            delta = b - a
            delta = str(delta).strip().split('days,')
            #print('resultim data',delta[0])
            if (delta[0].startswith("0:")==True):
                return 0
            else:
                return int(delta[0])

            
    def specialPercentHandling(self,entry):
        if isinstance(entry, float):

            return entry

        else:
            
            entry = str(entry)

            entry = entry.replace('%','')

            return int(entry)/100    
    
    def __init__(self):
        print('Init Called')
    
    def fit(self, X, y = None):
        print('fit called')
        
        return self

    def transform(self, X, y = None):
        print('Transform Called')
        
        X_ = X.copy()
        le = preprocessing.LabelEncoder()
        X_['alm_model'] = X_['alm_model'].astype(str)
        X_['alm_install_status'] = X_['alm_install_status'].astype(str)
        X_['alm_install_status'] = le.fit_transform(X_['alm_install_status'].values)    
        X_['alm_vendor'] = X_['alm_model'].apply(lambda x : self.getVendor(x))
        X_['alm_vendor'] = le.fit_transform(X_['alm_vendor'].values)
        #LABEL ENCONDE MODEL AFTER EXTRACT VENDOR
        X_['alm_model'] = le.fit_transform(X_['alm_model'].values)
        #df['SERIAL NUMBER'] = df['alm_display_name'].apply(lambda x : getDeviceId(x))
        #sourceCols.append('SERIAL NUMBER')
        #REPLACE FOR THE MOST FOUND
        X_['hardware_u_memory'] = X_['hardware_u_memory'].replace(np.nan,X_['hardware_u_memory'].value_counts().idxmax())
        X_['hardware_u_memory'] = X_['hardware_u_memory'].apply(lambda x : self.handlingMemoryData(x))
        #DROP NAN FOR HARDWARE PROCESSOR (293 lines on last dataset)
        X_.dropna(subset=['hardware_u_processor'])
        X_['hardware_u_processor'] = X_['hardware_u_processor'].astype(str)
        X_['hardware_u_processor'] = le.fit_transform(X_['hardware_u_processor'].values)   
        X_['alm_location.country'] = le.fit_transform(X_['alm_location.country'].values)
        X_['hardware_u_biometrics'] = X_['hardware_u_biometrics'].astype(str)
        #REPLACE FOR THE MOST FOUND
        X_['hardware_u_biometrics'] = X_['hardware_u_biometrics'].replace(np.nan,X_['hardware_u_biometrics'].value_counts().idxmax())
        X_['hardware_u_biometrics'] = le.fit_transform(X_['hardware_u_biometrics'].values) 
        #DATE TRANSFORM TO NUMBER OF DAYS
        now = datetime.now() # current date and time    
        X_['alm_x_ibmwa_ph_devic_est_asset_born_date'] = X_['alm_x_ibmwa_ph_devic_est_asset_born_date'].replace(np.nan,now.strftime("%Y-%m-%d %H:%M:%S"))
        X_['alm_x_ibmwa_ph_devic_est_asset_born_date'] = X_['alm_x_ibmwa_ph_devic_est_asset_born_date'].apply(lambda x : self.handlingDates(x))
        now = datetime.now() # current date and time
        #PERCENTAGE USED
        X_['mdm_disk_size'] = X_['mdm_disk_size'].astype(str)
        X_['mdm_disk_free_space'] = X_['mdm_disk_free_space'].astype(str)
        X_['mdm_disk_free_space'] = X_['mdm_disk_free_space'].str.strip().replace("'-1","0")
        X_['mdm_disk_size'] = X_['mdm_disk_size'].str.strip().replace("'-1","0")
        X_['mdm_disk_size'] = X_['mdm_disk_size'].astype(float)
        X_['mdm_disk_free_space'] = X_['mdm_disk_free_space'].astype(float)
        mean = X_['mdm_disk_free_space'].mean()
        X_['mdm_disk_free_space'] = X_['mdm_disk_free_space'].replace(0.0,mean)
        mean = X_['mdm_disk_size'].mean()
        X_['mdm_disk_size'] = X_['mdm_disk_size'].replace(0.0,mean)
        X_['mdm_disk_usage'] = (X_['mdm_disk_size'] - X_['mdm_disk_free_space'])/X_['mdm_disk_size']
        X_['mdm_times_deployed'] = X_['mdm_times_deployed'].astype(int)
                      
        #if (y.empty==False):
            #y_ = y.copy()
            #y_= y_.apply(lambda x : self.specialPercentHandling(x))
            
        print('Transform Finished')
        
        return X_
