import aiohttp
import asyncio
from components import app, page_sources
from fake_useragent import UserAgent, FakeUserAgentError
from flask import render_template, request, session, g

QUANTA_MAGAZINE = 'QuantaMagazine'
REUTERS = 'Reuters'
TECH_CRUNCH = 'TechCrunch'
WIRED = 'Wired'
BBC = 'BBC'
THE_VERGE = 'TheVerge'
BUZZFEED = 'BuzzFeed'
NY_TIMES = 'The New York Times'
TNW = 'The Next Web'

home_content_sources = [ QUANTA_MAGAZINE, WIRED, REUTERS, TECH_CRUNCH, BBC, THE_VERGE ]
tech_content_sources = [ THE_VERGE, TECH_CRUNCH, REUTERS, BUZZFEED, TNW, NY_TIMES ]
science_content_sources = [ QUANTA_MAGAZINE, REUTERS, THE_VERGE ]
# app.secret_key = "MySecretKey1234"
# asyncio.set_event_loop(asyncio.new_event_loop())

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


# @app.before_first_request
# def set_event_loop():
    # asyncio.set_event_loop(asyncio.new_event_loop())
    # session['enent_loop'] = asyncio.new_event_loop()
    # asyncio.set_event_loop(session['enent_loop'])


@app.route('/')
@app.route('/home',methods=['GET'])
def home():

    sources = page_sources.Home(home_content_sources).sources

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(fetch_sources(sources))

    populate_sources(sources,responses)
    responses = None

    # for source in sources:
    #     print("***************")
    #     print(source.posts)
    #     print(source.posts_desc)
    return render_template('posts.htm',sources=sources)


@app.route('/tech')
def tech_posts():
    sources = page_sources.Tech(tech_content_sources).sources

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(fetch_sources(sources))

    populate_sources(sources,responses)
    responses = None

    return render_template('posts.htm',sources=sources)