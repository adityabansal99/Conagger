import aiohttp
import asyncio
from components import app, source
from components import source
from flask import request

QUANTA_MAGAZINE = 'quantamagazine'
REUTERS = 'reuters'
TECH_CRUNCH = 'techcrunch'
WIRED = 'wired'

source_uri = {
    QUANTA_MAGAZINE  : 'https://www.quantamagazine.org/',
    REUTERS          : 'https://www.reuters.com/',
    TECH_CRUNCH      : 'https://www.techcrunch.com/',
    WIRED            : 'https://www.wired.com/',
}


async def fetch_source_response(session,url):
    async with session.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}) as response:
        body = (await response.text())
        return body


async def fetch_sources_response(content_sources):
    responses = []
    async with aiohttp.ClientSession() as session:
        for content_source in content_sources:
            resp_body = asyncio.ensure_future(fetch_source_response(session,content_source.uri))
            responses.append(resp_body)
            content_source.response = resp_body
        await asyncio.gather(*responses, return_exceptions=True)


def make_sources(content_sources):
    sources = []
    if QUANTA_MAGAZINE in content_sources:
        sources.append(source.QuantaMagazine(source_uri[QUANTA_MAGAZINE]))
    if REUTERS in content_sources:
        sources.append(source.Reuters(source_uri[REUTERS]))
    if TECH_CRUNCH in content_sources:
        sources.append(source.TechCrunch(source_uri[TECH_CRUNCH]))
    if WIRED in content_sources:
        sources.append(source.Wired(source_uri[WIRED]))


@app.route('/')
def index():
    return 'Hello World'


@app.route('/home',methods=['POST'])
def home():
    content_sources = request.form.get('content_sources').split(',')
    sources = make_sources(content_sources)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_sources_response(sources))

    
    return "Completed"


