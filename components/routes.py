import aiohttp
import asyncio
from components import app, source
from components import source
from fake_useragent import UserAgent
from flask import render_template, request

QUANTA_MAGAZINE = 'QuantaMagazine'
REUTERS = 'Reuters'
TECH_CRUNCH = 'TechCrunch'
WIRED = 'Wired'
BBC = 'BBC'
THE_VERGE = 'TheVerge'

source_uri = {
    QUANTA_MAGAZINE  : 'https://www.quantamagazine.org',
    REUTERS          : 'https://www.reuters.com',
    TECH_CRUNCH      : 'https://www.techcrunch.com',
    WIRED            : 'https://www.wired.com',
    BBC              : 'https://www.bbc.com',
    THE_VERGE        : 'https://www.theverge.com',
}


def instantiate_sources(content_sources):
    sources = []
    if QUANTA_MAGAZINE in content_sources:
        sources.append(source.QuantaMagazine(source_uri[QUANTA_MAGAZINE],QUANTA_MAGAZINE))
    if REUTERS in content_sources:
        sources.append(source.Reuters(source_uri[REUTERS],REUTERS))
    if TECH_CRUNCH in content_sources:
        sources.append(source.TechCrunch(source_uri[TECH_CRUNCH],TECH_CRUNCH))
    if WIRED in content_sources:
        sources.append(source.Wired(source_uri[WIRED],WIRED))
    if BBC in content_sources:
        sources.append(source.BBC(source_uri[BBC],BBC))
    if THE_VERGE in content_sources:
        sources.append(source.TheVerge(source_uri[THE_VERGE],THE_VERGE))
    return sources


def populate_sources(sources,responses):
    for source in sources:
        source.response = responses[source.uri].result()


async def fetch_source(session,url,headers):
    async with session.get(url,headers=headers) as response:
        body = (await response.text())
        return body


async def fetch_sources(sources):
    responses = dict()
    headers = None
    try:
        ua = UserAgent(cache=False)
        user_agent = ua.random
        headers = {'User-Agent': user_agent}
    except FakeUserAgentError:
        headers = None

    async with aiohttp.ClientSession() as session:
        for source in sources:
            resp_body = asyncio.ensure_future(fetch_source(session,source.uri,headers))
            responses[source.uri] = resp_body
        await asyncio.gather(*responses.values(), return_exceptions=True)
    return responses


@app.route('/')
def index():
    return 'Hello World'


@app.route('/home',methods=['GET','POST'])
def home():
    # content_sources = request.form.get('content_sources').split(',')
    content_sources = ['QuantaMagazine','Wired','Reuters','TechCrunch','BBC','TheVerge']
    sources = instantiate_sources(content_sources)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(fetch_sources(sources))

    populate_sources(sources,responses)
    
    # for source in sources:
    #     print(source.posts)
    #     print('***************')
    return render_template('base.htm',sources=sources)


@app.route('/test')
def test_jinja():
    items = [1,2,3,4,5,6,7,8]
    return render_template('test.htm',items=items)