# STEP 1: DATA GENERATION
from data_generation.genesis import genesis_bulk_global

genesis_file_path = '/home/think/Desktop/TESIS/test_runs/templates/global_test.json'
destination_path = "/home/think/Desktop/TESIS/test_runs"
'''
So, first we have to generate the data
file_path tells us where our blueprint is and welp, we have to
edit it everytime (unless we develop architect.py)
and destination path is just to keep a record.
'''
# right now it doesn't store, it's in echo mode
'''
We have to check the conditions for the parameters and the ranges where
the data will make sense, for example some of these systems can't generate chaos
untill a certain time and it's expensive, so we have to look into that.
'''
genesis_bulk_global(genesis_file_path, destination_path)

#BTW, THIS SHIT DOESNT STOP BY ITSLEF, FIX THAT!!!!!!!!!

# STEP 2: DATA PREPARATION
from utils.helpers import crawler
from scripts.utils.plastic_surgeon import transition

'''
Okay, so at this point we have the data generated stored a certain way and
we may or not want to access the data that certain way, so we can encode that 
structure in the genesis function or we can fee it to crawler.
Crawler will do 2 things, crawl the data and feed it into 
'''
configuration_file_path = ''



df_raw = crawler(configuration_file_path)
df = transition(df_raw)

# STEP 3: DATA PROCESSING
from data_generation.predictions import predictions_enssemble
test_days = 60 # pues decidimos el forecasting window
predictions_enssemble(df,test_days) # esto nos regresa un diccionario

# STEP 4: DATA AND METRICS STORAGE
'''
Welp, i guess to make it easy we have to keep it connected and
we only have to store 1 df per sample which will include 
the test sample and the predictions of each of the models used 
also we have to store info from where the data used comes from and where is it?
'''