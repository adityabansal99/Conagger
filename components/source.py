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

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self,resp):
        self._response = resp
        # print(resp)
        self._soup = bs4.BeautifulSoup(resp,"html.parser")
        self._parse()

    @property
    def posts(self):
        return self._posts

    @property
    def source_name(self):
        return self._source_name

    def _parse(self):
        raise NotImplementedError("Parse Method is not implemented for source: ",type(self).__name__)



class QuantaMagazine(Source):
    """
    QuantaMagazine content parsing and management
    """
    _home_uri = 'https://www.quantamagazine.org'

    @classmethod
    def create_for_home(cls,source_name):
        return cls(cls._home_uri, source_name)


    def _parse(self):
        if self._uri == QuantaMagazine._home_uri:
            self._parse_for_home()
        else:
            raise NotImplementedError("Parse method not implemented for given uri:",self._uri)

    def _parse_for_home(self):

        # Main post 
        self._posts[self._soup.select("h1.noe:nth-child(1)")[0].get_text().strip()] = self._uri + self._soup.select(".hero-title > a")[0]['href']
    
        # div.home__posts--top > div > div > div.card__content > a > h2
        posts_text = [
            heading.get_text().strip() 
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
    _home_uri = 'https://www.reuters.com'
    _tech_uri = 'https://www.reuters.com/news/technology'

    @classmethod
    def create_for_home(cls,source_name):
        return cls(cls._home_uri,source_name)

    @classmethod
    def create_for_tech(cls,source_name):
        return cls(cls._tech_uri,source_name)


    def _parse(self):
        if self._uri == Reuters._home_uri:
            self._parse_for_home()
        elif self._uri == Reuters._tech_uri:
            self._parse_for_tech()
        else:
            raise NotImplementedError("Parse method not implemented for given uri:",self._uri)

    def _parse_for_home(self):
        
        # Main Post
        self._posts[self._soup.select("section.right-now-module > div:nth-child(2) > h2 > a")[0].get_text().strip()] = \
        self._uri + self._soup.select("section.right-now-module > div:nth-child(2) >h2 > a")[0]['href']

        posts_text = [
            heading.get_text().strip() 
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
    _home_uri = 'https://www.techcrunch.com'
    _tech_uri = 'https://www.techcrunch.com'

    @classmethod
    def create_for_home(cls,source_name):
        return cls(cls._home_uri,source_name)

    @classmethod
    def create_for_tech(cls,source_name):
        return cls(cls._tech_uri,source_name)


    def _parse(self):
        if self._uri == TechCrunch._home_uri:
            self._parse_for_home()
        elif self._uri == TechCrunch._tech_uri:
            self._parse_for_tech()
        else:
            raise NotImplementedError("Parse method not implemented for given uri:",self._uri)

    def _parse_for_home(self):
        
        #root > div > div > div > div > div > header > h2 > a
        posts_text = [
            heading.get_text().strip() 
            for heading in self._soup.select("#root > div > div > div > div > div > header > h2 > a")
        ]
        posts_link =[
            link['href'] 
            for link in self._soup.select("#root > div > div > div > div > div > header > h2 > a")
        ]

        # Will refactor later
        posts_text = posts_text[:6]
        posts_link = posts_link[:6]

        for post_text, post_link in zip(posts_text,posts_link):
            self._posts[post_text] = post_link



class Wired(Source):
    """
    Wired content parsing and management
    """
    _home_uri = 'https://www.wired.com'

    @classmethod
    def create_for_home(cls,source_name):
        return cls(cls._home_uri,source_name)
    

    def _parse(self):
        if self._uri == Wired._home_uri:
            self._parse_for_home()
        else:
            raise NotImplementedError("Parse method not implemented for given uri:",self._uri)

    def _parse_for_home(self):
        
        # div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div > ul > li:nth-child(2) > a:nth-child(2)
        posts_text = [
                heading.get_text().strip() 
                for heading in self._soup.select("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div > ul > li:nth-child(2) > a:nth-child(2) > h2")
        ] + [
                heading.get_text().strip() 
                for heading in self._soup.select("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div >div> ul > li:nth-child(2) > a:nth-child(2) > h2")
        ]
        posts_relative_link =[
            link['href'] 
            for link in self._soup.select("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div > ul > li:nth-child(2) > a:nth-child(2)")
        ] + [
            link['href'] 
            for link in self._soup.select("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div >div> ul > li:nth-child(2) > a:nth-child(2)")
        ]

        for post_text, post_relative_link in zip(posts_text,posts_relative_link):
            self._posts[post_text] = self._uri + post_relative_link



class TheVerge(Source):
    """
    TheVerge content management and parsing
    """
    _home_uri = 'https://www.theverge.com'
    _tech_uri = 'https://www.theverge.com/tech'

    @classmethod
    def create_for_home(cls,source_name):
        return cls(cls._home_uri,source_name)

    @classmethod
    def create_for_tech(cls,source_name):
        return cls(cls._tech_uri,source_name)


    def _parse(self):
        if self._uri == TheVerge._home_uri:
            self._parse_for_home()
        elif self._uri == TheVerge._tech_uri:
            self._parse_for_tech()
        else:
            raise NotImplementedError("Parse method not implemented for given uri:",self._uri)

    def _parse_for_home(self):

        # div.c-seven-up__main > div > div:nth-child(2) > h2 > a
        posts_text = [
            heading.get_text().strip() 
            for heading in self._soup.select("div.c-seven-up__main > div > div:nth-child(2) > h2 > a")
        ]
        posts_link =[
            link['href'] 
            for link in self._soup.select("div.c-seven-up__main > div > div:nth-child(2) > h2 > a")
        ]
        
        # Will refactor later
        posts_text = posts_text[:6]
        posts_link = posts_link[:6]

        for post_text, post_link in zip(posts_text,posts_link):
            self._posts[post_text] = post_link
        


class BBC(Source):
    """
    BBC content management and parsing
    """
    _home_uri = 'https://www.bbc.com'

    @classmethod
    def create_for_home(cls,source_name):
        return cls(cls._home_uri,source_name)


    def _parse(self):
        if self._uri == BBC._home_uri:
            self._parse_for_home()
        else:
            raise NotImplementedError("Parse method not implemented for given uri:",self._uri)

    def _parse_for_home(self):

        # Does not pick reels posts
        # ul.media-list > li > div > a:nth-child(3)
        posts_text = [
            heading.get_text().strip() 
            for heading in self._soup.select("ul.media-list > li > div > a:nth-child(3)")
        ]
        posts_link =[
            link['href'] 
            for link in self._soup.select("ul.media-list > li > div > a:nth-child(3)")
        ]

        # Will refactor later
        posts_text = posts_text[:6]
        posts_link = posts_link[:6]

        for post_text, post_link in zip(posts_text,posts_link):
            self._posts[post_text] = post_link



class BuzzFeed(Source):
    """
    BuzzFeed content management and parsing
    """
    _tech_uri = 'https://www.buzzfeed.com/tech'

     @classmethod
    def create_for_tech(cls,source_name):
        return cls(cls._tech_uri,source_name)


    def _parse(self):
        if self._uri == BuzzFeed._tech_uri:
            self._parse_for_tech()
        else:
            raise NotImplementedError("Parse method not implemented for given uri:",self._uri)

    def  _parse_for_tech(self):
        pass



class TheNewYorkTimes(Source):
    """
    BuzzFeed content management and parsing
    """
    _tech_uri = 'https://www.nytimes.com/section/technology'

     @classmethod
    def create_for_tech(cls,source_name):
        return cls(cls._tech_uri,source_name)


    def _parse(self):
        if self._uri == TheNewYorkTimes._tech_uri:
            self._parse_for_tech()
        else:
            raise NotImplementedError("Parse method not implemented for given uri:",self._uri)

    def  _parse_for_tech(self):
        pass



class TheNextWeb(Source):
    """
    BuzzFeed content management and parsing
    """
    _tech_uri = 'https://thenextweb.com/'

     @classmethod
    def create_for_tech(cls,source_name):
        return cls(cls._tech_uri,source_name)


    def _parse(self):
        if self._uri == TheNextWeb._tech_uri:
            self._parse_for_tech()
        else:
            raise NotImplementedError("Parse method not implemented for given uri:",self._uri)

    def  _parse_for_tech(self):
        pass