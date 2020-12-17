import bs4

class Source():
    """
    Base class for all content sources
    Should not be used to instantiate objects
    """
    def __init__(self,uri,source_name):
        self._uri = uri
        self._posts = dict()
        self._source_name = source_name

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self,uri_val):
        self._uri = uri_val

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self,resp):
        if resp.ok:
            self._response = resp
            self._soup = bs4.BeautifulSoup(resp.content,"html.parser")
            self._parse()
        else:
            raise ValueError("Something went wrong with response received from "+resp.url+". Reson: "+resp.reason)

    @property
    def posts(self):
        return self._posts

    @property
    def source_name(self):
        return self._source_name

    def _parse(self):
        raise NotImplementedError("Parse Method is not implemented for source:",type(self).__name__)


class QuantaMagazine(Source):
    """
    QuantaMagazine content parsing and management
    """
    def _parse(self):

        # Main post 
        self._posts[self._soup.select("h1.noe:nth-child(1)")[0].get_text()] = self._uri + self._soup.select(".hero-title > a")[0]['href']
    
        # div.home__posts--top > div > div > div.card__content > a > h2
        posts_text = [
            heading.get_text() 
            for heading in self._soup.select("div.two--large > div:nth-child(1) > div:nth-child(2) > a:nth-child(2) > h2:nth-child(1)")
        ]
        posts_relative_link =[
            link['href'] 
            for link in self._soup.select("div.two--large > div:nth-child(1) > div:nth-child(2) > a")
        ]

        for post_text, post_relative_link in zip(posts_text,posts_relative_link):
            self._posts[post_text] = self._uri + post_relative_link




class Reuters(Source):
    """
    Reuters content parsing and management
    """
    def _parse(self):
        
        # Main Post
        self._posts[self._soup.("section.right-now-module > div:nth-child(2) > h2 > a")[0].get_text()] = \
        self._uri + self._soup.select("section.right-now-module > div:nth-child(2) >h2 > a")[0]['href']

        posts_text = [
            heading.get_text() 
            for heading in self._soup.select("#hp-top-news-top > section > div > article > div > a > h3")
        ]
        posts_relative_link =[
            link['href'] 
            for link in self._soup.select("#hp-top-news-top > section > div > article > div > a")
        ]

        for post_text, post_relative_link in zip(posts_text,posts_relative_link):
            self._posts[post_text] = self._uri + post_relative_link
        


class TechCrunch(Source):
    """
    TechCrunch content parsing and management
    """
    def _parse(self):
        
        #root > div > div > div > div > div > header > h2 > a
        posts_text = [
            heading.get_text() 
            for heading in self._soup.select("#root > div > div > div > div > div > header > h2 > a")
        ]
        posts_link =[
            link['href'] 
            for link in self._soup.select("#hp-top-news-top > section > div > article > div > a")
        ]

        for post_text, post_link in zip(posts_text,posts_link):
            self._posts[post_text] = post_link


class Wired(Source):
    """
    Wired content parsing and management
    """
    def _parse(self):
        
    #div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div > ul > li:nth-child(2) > a:nth-child(2)

    posts_text = [
            heading.get_text() 
            for heading in self._soup.select("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div > ul > li:nth-child(2) > a:nth-child(2) > h2")
        ] + [
            heading.get_text() 
            for heading in self._soup.select("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div >div> ul > li:nth-child(2) > a:nth-child(2) > h2")
        ]
        posts_relative_link =[
            link['href'] 
            for link in self._soup.select("#div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div > ul > li:nth-child(2) > a:nth-child(2)")
        ] + [
            link['href'] 
            for link in self._soup.select("#div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div >div> ul > li:nth-child(2) > a:nth-child(2)")
        ]

        for post_text, post_relative_link in zip(posts_text,posts_relative_link):
            self._posts[post_text] = self._uri + post_relative_link