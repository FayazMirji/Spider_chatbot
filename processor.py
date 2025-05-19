
import json
import os
import asyncio
import aiomysql

DB_CONFIG={
    "host":"localhost",
    "user":"root",
    "password":"password",
    "db":"fed_registers",
}

async def insert_docs(pool,docs):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for doc in docs:
                await cur.execute("""
                    INSERT INTO documents (document_number, title, publication_date, agency_names, url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE title=VALUES(title)
                """, (
                    doc["document_number"],
                    doc["title"],
                    doc["publication_date"],
                    ", ".join(doc["agency_names"]),
                    doc["html_url"]
                ))
            await conn.commit()

async def process_and_store(filename):
    with open(f"raw_data/{filename}","r") as f:
        data=json.load(f)


    pool=await aiomysql.create_pool(**DB_CONFIG)
    await insert_docs(pool, data)
    pool.close()
    await pool.wait_closed()

if __name__=='main':
    asyncio.run(process_and_store("2025-05-17.json"))

