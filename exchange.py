import aiohttp

CBR_API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


async def get_currency():
    async with aiohttp.ClientSession() as session:
        async with session.get(CBR_API_URL) as response:
            if response.status != 200:
                return None

            data = await response.json(content_type=None)
            return data