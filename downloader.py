
import aiohttp
import asyncio
import json 
import os
from datetime import date

import aiohttp
print(aiohttp.__version__)
import sys
print(sys.executable)



Base_url="https://www.federalregister.gov/api/v1/documents.json"

async def fetch_data(start_date:'str',end_date:'str',per_page:int=100):
    params={'per_page':per_page,
            'order':'new_order',
            'conditions[publication_date][gte]':start_date,
            'conditions[publication_date][lte]':end_date
            }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(Base_url,params=params)as response:
            data= await response.json()
            return data.get('results',[])
        
async def save_raw_data(data, filename):
    os.makedir("raw_data",exit_ok=True)
    path=f"raw_data/{filename}"
    with open(path,"w") as f:
        json.dump(data,f,indent=2)
    print('save raw data to path')

async def run_downloader():
    today=date.today()
    start=today.replace(day=1).isoformat()
    end=today.isoformat()
    data=await fetch_data(start,end)
    await save_raw_data(data,f"{end}.json")

if __name__ =="main":
    asyncio.run(run_downloader())

        
