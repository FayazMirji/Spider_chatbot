import aiomysql

DB_CONFIG={
    "host":"localhost",
    "user":"root",
    "password":"password",
    "db":"fed_register",
}


async def fetch_documents_by_agency(agency:str):
    pool=await aiomysql.create_pool(**DB_CONFIG)
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.dictCursor) as cur:
            await cur.execute("""
                              SELECT title, publuvcation_date, url
                              FROM documents
                              WHERE agency_names LIKE %s
                              ORDER BY publication_date DESC
                              LIMIT 5
                              """,(f"%{agency}%",))
            
            result=await cur.fetchall()
    pool.close()
    await pool.wait_closed()
    return result
    