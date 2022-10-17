#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
from datetime import datetime
import os
from web3 import Web3
with open("./key/infura.txt", "r") as f:
    RPC_ENDPOINT = f.read().strip()
    
w3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))

FOLDER = "/home/ubuntu/mevboost.pics/scripts/enriched_data/"
PROJECT = "/home/ubuntu/mevboost.pics/scripts/"
DATAFARM = "/home/ubuntu/ethereum-datafarm/data/"


# In[8]:


tornado_txs = []
for i in os.listdir(DATAFARM):
    if "tornado" in i:
        for j in os.listdir(DATAFARM+i):
            #print("../ethereum-datafarm/data/"+i + "/" + j)
            _df = pd.read_csv(DATAFARM+i + "/" + j, index_col=0)
            _df = _df[_df["timestamp"] >= 1663221600]["txhash"].tolist()
            tornado_txs.extend(_df)
tornado_txs = set(tornado_txs)
len(tornado_txs)

tmp = []
for i in os.listdir(FOLDER):
    if "mevboost_e_txs" in i:
        tmp.append(pd.read_csv(FOLDER + i))
ee = pd.concat(tmp, ignore_index=True)


# In[9]:


ee.drop_duplicates()


# In[3]:


tornado_in_mev = ee[ee["txhash"].isin(tornado_txs)].reset_index(drop=True)
tornado_in_mev.to_csv(FOLDER + "mevboost_e_txs_0.csv", index=None)
tornado_blocks = set(tornado_in_mev["block_number"])


# In[4]:


for i in os.listdir(FOLDER):
    if "mevboost_e_txs" in i and i != "mevboost_e_txs_0.csv":
        os.remove(FOLDER + i)   


# In[5]:


tornado_in_mev = tornado_in_mev.groupby("block_number").count().drop("miner", axis = 1)


# In[14]:


df = pd.read_csv(FOLDER + "mevboost_e.csv", dtype={"value":float, "slot":int, "gas_limit": str,
                                                   "block_number": int, "gas_used": float}).set_index("block_number")
df = df[~df["miner"].isna()]
with open(PROJECT+"tornado_latest_known_block.txt", "w") as file:
    file.write(str(max(df["slot"])))
total = df.groupby("relay")["slot"].count()


# In[ ]:


tdf = df.join(tornado_in_mev)


# In[ ]:


tdf = tdf[~tdf["txhash"].isna()]
tdf.to_csv(PROJECT+"tornadothroughmev.csv")


# In[ ]:


total_tornado = tdf.groupby("relay")["slot"].count()


# In[ ]:


df_lastDay = tdf[tdf["slot"] >= max(df["slot"])-7200] # 7200*12=86400
df_lastDay = df_lastDay.groupby("relay")["slot"].count()


# In[ ]:


df_last30Day = tdf[tdf["slot"] >= max(df["slot"])-(7200*30)]
df_last30Day = df_last30Day.groupby("relay")["slot"].count()


# In[ ]:


df_last14Day = tdf[tdf["slot"] >= max(df["slot"])-(7200*14)]
df_last14Day = df_last14Day.groupby("relay")["slot"].count()


# In[ ]:


df_all = pd.DataFrame(total).join(pd.DataFrame(total_tornado), lsuffix="_total")
df_all = df_all.join(pd.DataFrame(df_last30Day), rsuffix="_30_days")
df_all = df_all.join(pd.DataFrame(df_lastDay), rsuffix="_1_day")
df_all = df_all.join(pd.DataFrame(df_last14Day), rsuffix="_14_day")
    

df_all = df_all.fillna(0)
df_all.reset_index().to_csv(PROJECT+"tornado_stats.csv", index=None)


# In[ ]:


print(datetime.strftime(datetime.now(), "%Y-%m-%d, %I:%M %p") + " - tornado preparation")

