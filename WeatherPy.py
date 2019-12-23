# %%
import random
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

# %%
lats = np.random.uniform(-90.0,90.0,size=1500)
lngs = np.random.uniform(-180.0,180.0,size=1500)

lats_lngs = zip(lats, lngs)
coordinates = list(lats_lngs)
print(coordinates[:11])

# %%
