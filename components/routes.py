from components import app
import bs4
import aiohttp
import asyncio
from flask import request


source_uri = {
    'reddit'          : 'https://www.reddit.com',
    'wired'           : 'https://www.wired.com/',
    'reuters'         : 'https://www.reuters.com/',
    'techcrunch'      : 'https://www.techcrunch.com/',
    'quantamagazine'  : 'https://www.quantamagazine.org/'
}

@app.route('/')
def index():
    return 'Hello World'


@app.route('/home',methods=['POST'])
def home():
    content_sources = request.form.get('content_sources')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_sources((source_uri[source] for source in content_sources.split(','))))
    return "Completed"



async def fetch_source(session,url):
    async with session.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}) as response:
        print(response.url)
        return response

async def fetch_sources(sources):
    responses = []
    async with aiohttp.ClientSession() as session:
        for url in sources:
            resp = asyncio.ensure_future(fetch_source(session,url))
            responses.append(resp)
        await asyncio.gather(*responses, return_exceptions=True)
    for response in responses:
        print(response.result())