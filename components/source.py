import bs4

class Source():
    """
    Base class for all content sources
    Should not be used to instantiate objects
    """
    _home_uri = None
    _tech_uri = None
    _science_uri = None

    def __init__(self,uri,source_name):
        self._uri = uri
        self._posts = dict()
        self._posts_desc = dict()
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

    @property
    def posts_desc(self):
        return self._posts_desc

    @classmethod
    def create_for_home(cls,source_name):
        if cls._home_uri == None:
            raise NotImplementedError(cls.__name__+" does not support home configuration")
        return cls(cls._home_uri, source_name)

    @classmethod
    def create_for_science(cls,source_name):
        if cls._science_uri == None:
            raise NotImplementedError(cls.__name__+" does not support science configuration")
        return cls(cls._science_uri, source_name)

    @classmethod
    def create_for_tech(cls,source_name):
        if cls._tech_uri == None:
            raise NotImplementedError(cls.__name__+" does not support tech configuration")
        return cls(cls._tech_uri,source_name)

    def _get_titles(self,css_selector):
        posts_title = [
            heading.get_text().strip() 
            for heading in self._soup.select(css_selector)
        ]
        return posts_title

    def _get_links(self,css_selector):
        posts_link = [
            link['href'] 
            for link in self._soup.select(css_selector)
        ]
        return posts_link

    def _get_descriptions(self,css_selector):
        posts_desc = [
            desc.get_text().strip() 
            for desc in self._soup.select(css_selector)
        ]
        return posts_desc

    def _set_posts_and_desc(self, posts_text, posts_link, posts_desc=None, desc_available=True, link_relative=False):
        if desc_available:
            for post_text, post_link, post_desc in  zip(posts_text, posts_link, posts_desc):
                if link_relative:
                    self._posts[post_text] = type(self)._home_uri + post_link
                else:
                    self._posts[post_text] = post_link
                self._posts_desc[post_text] = post_desc
        else:
            for post_text, post_link in  zip(posts_text, posts_link):
                if link_relative:
                    self._posts[post_text] = type(self)._home_uri + post_link
                else:
                    self._posts[post_text] = post_link


    def _parse(self):
        if self._uri == type(self)._home_uri:
            self._parse_for_home()
        elif self._uri == type(self)._tech_uri:
            self._parse_for_tech()
        elif self._uri == type(self)._science_uri:
            self._parse_for_science()
        else:
            raise NotImplementedError("Parse method not implemented for given uri: "+self._uri+" by "+self._source_name)



class QuantaMagazine(Source):
    """
    QuantaMagazine content parsing and management
    """
    _home_uri = 'https://www.quantamagazine.org'
    _science_uri = 'https://www.quantamagazine.org'


    def _parse_for_home(self):

        # Main post 
        self._posts[self._get_titles("h1.noe:nth-child(1)")[0]] = QuantaMagazine._home_uri + self._get_links(".hero-title > a")[0]
        self._posts_desc[self._get_titles("h1.noe:nth-child(1)")[0]] = self._get_descriptions("div.cws__content > div:nth-child(1) > div.p > small > span > p")[0]

        # div.home__posts--top > div > div > div.card__content > a > h2
        posts_text = self._get_titles("div.two--large > div:nth-child(1) > div:nth-child(2) > a:nth-child(2) > h2:nth-child(1)")
        
        posts_relative_link = self._get_links("div.two--large > div:nth-child(1) > div:nth-child(2) > a")

        posts_desc = self._get_descriptions("div.two--large > div:nth-child(1) > div:nth-child(2) > div.card__excerpt >p")

        self._set_posts_and_desc(posts_text, posts_relative_link, posts_desc=posts_desc, link_relative=True)

    def _parse_for_science(self):
        self._parse_for_home()



class Reuters(Source):
    """
    Reuters content parsing and management
    """
    _home_uri = 'https://www.reuters.com'
    _tech_uri = 'https://www.reuters.com/news/technology'
    _science_uri = 'https://www.reuters.com/news/science'


    def _parse_for_home(self):
        # Main Post
        # self._posts[self._get_titles("section.right-now-module > div:nth-child(2) > h2 > a")[0]] = \
            # Reuters._home_uri + self._get_links("section.right-now-module > div:nth-child(2) >h2 > a")[0]

        # self._posts_desc[self._get_titles("section.right-now-module > div:nth-child(2) > h2 > a")[0]] = \
            # self._get_descriptions("section.right-now-module > div:nth-child(2) > p")[0]

        # posts_text = self._get_titles("#hp-top-news-top > section > div > article > div > a > h3")
        posts_text = self._get_titles("span[class^='MediaStoryCard']")
        
        # posts_relative_link =self._get_links("#hp-top-news-top > section > div > article > div > a")
        posts_relative_link =self._get_links("a[class^='MediaStoryCard']")

        self._set_posts_and_desc(posts_text, posts_relative_link, desc_available=False, link_relative=True)


    def _parse_for_tech(self):
        posts_text = self._get_titles("#content > section:nth-child(4) > div > div.column1 > section.module > section > div > article > div:nth-child(2) > a:nth-child(1)> h3")
        
        posts_relative_link = self._get_links("#content > section:nth-child(4) > div > div.column1 > section.module > section > div > article > div:nth-child(2) > a:nth-child(1)")

        posts_desc = self._get_descriptions("#content > section:nth-child(4) > div > div.column1 > section.module > section > div > article > div:nth-child(2) > p")

        self._set_posts_and_desc(posts_text, posts_relative_link, posts_desc=posts_desc, link_relative=True)


    def _parse_for_science(self):
        posts_text = self._get_titles("#content > section:nth-child(4) > div > div.column1 > section.module > section > div > article > div:nth-child(2) > a:nth-child(1)> h3")
        
        posts_relative_link = self._get_links("#content > section:nth-child(4) > div > div.column1 > section.module > section > div > article > div:nth-child(2) > a:nth-child(1)")

        posts_desc = self._get_descriptions("#content > section:nth-child(4) > div > div.column1 > section.module > section > div > article > div:nth-child(2) > p")

        self._set_posts_and_desc(posts_text, posts_relative_link, posts_desc=posts_desc, link_relative=True)


class TechCrunch(Source):
    """
    TechCrunch content parsing and management
    """
    _home_uri = 'https://www.techcrunch.com'
    _tech_uri = 'https://www.techcrunch.com'


    def _parse_for_home(self):
        
        #root > div > div > div > div > div > header > h2 > a
        posts_text = self._get_titles("#root > div > div > div > div > div > header > h2 > a")
        
        posts_link =self._get_links("#root > div > div > div > div > div > header > h2 > a")
        
        posts_desc = [
            desc.get_text().strip() 
            for desc in self._soup.select("#root > div > div > div > div > div > div")
        ]

        self._set_posts_and_desc(posts_text, posts_link, posts_desc=posts_desc)
    
    def _parse_for_tech(self):
        self._parse_for_home()



class Wired(Source):
    """
    Wired content parsing and management
    """
    _home_uri = 'https://www.wired.com'
  

    def _parse_for_home(self):
        
        # div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div > ul > li:nth-child(2) > a:nth-child(2)
        posts_text = list(self._get_titles("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div > ul > li:nth-child(2) > a:nth-child(2) > h2") + 
                self._get_titles("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div >div> ul > li:nth-child(2) > a:nth-child(2) > h2"))
        
        posts_relative_link = list(self._get_links("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div > ul > li:nth-child(2) > a:nth-child(2)")
        + self._get_links("div.homepage-main > div.primary-grid-component > div > div.cards-component > div.cards-component__row > div > div >div> ul > li:nth-child(2) > a:nth-child(2)"))

        self._set_posts_and_desc(posts_text, posts_relative_link, desc_available=False, link_relative=True)



class TheVerge(Source):
    """
    TheVerge content management and parsing
    """
    _home_uri = 'https://www.theverge.com'
    _tech_uri = 'https://www.theverge.com/tech'
    _science_uri = 'https://www.theverge.com/science'


    def _parse_for_home(self):

        # div.c-seven-up__main > div > div:nth-child(2) > h2 > a
        posts_text = self._get_titles("div.c-seven-up__main > div > div:nth-child(2) > h2 > a")
        
        posts_link =self._get_links("div.c-seven-up__main > div > div:nth-child(2) > h2 > a")
        
        for post_text, post_link in zip(posts_text,posts_link):
            self._posts[post_text] = post_link


    def _parse_for_tech(self):
        posts_text = list(self._get_titles("div.l-hero > section > div > div > div > h3 > a") + 
        self._get_titles("div.l-reskin > div > div > div:nth-child(1) > div > div > div > div:nth-child(2) > h2 > a"))
        
        posts_link = list(self._get_links("div.l-hero > section > div > div > div > h3 > a")
        + self._get_links("div.l-reskin > div > div > div:nth-child(1) > div > div > div > div:nth-child(2) > h2 > a"))

        self._set_posts_and_desc(posts_text, posts_link, desc_available=False)


    def _parse_for_science(self):
        posts_text = list(self._get_titles("div.l-hero > section > div > div > div > h3 > a") + 
        self._get_titles("div.l-reskin > div > div > div:nth-child(1) > div > div > div > div:nth-child(2) > h2 > a"))
        
        posts_link = list(self._get_links("div.l-hero > section > div > div > div > h3 > a")
        + self._get_links("div.l-reskin > div > div > div:nth-child(1) > div > div > div > div:nth-child(2) > h2 > a"))

        self._set_posts_and_desc(posts_text, posts_link, desc_available=False)



class BBC(Source):
    """
    BBC content management and parsing
    """
    _home_uri = 'https://www.bbc.com'


    def _parse_for_home(self):

        # Does not pick reels posts
        # ul.media-list > li > div > a:nth-child(3)
        posts_text = self._get_titles("ul.media-list > li > div > a:nth-child(3)")
        
        posts_link =self._get_links("ul.media-list > li > div > a:nth-child(3)")

        self._set_posts_and_desc(posts_text, posts_link, desc_available=False)



class BuzzFeed(Source):
    """
    BuzzFeed content management and parsing
    """
    _home_uri = 'https://www.buzzfeed.com'
    _tech_uri = 'https://www.buzzfeed.com/tech'


    def  _parse_for_tech(self):
        posts_text = self._get_titles("#buzz-content > div > div.feed-cards > article > div:nth-child(3) > div > h2> a")
        
        posts_link = self._get_links("#buzz-content > div > div.feed-cards > article > div:nth-child(3) > div > h2> a")
        
        posts_desc = self._get_descriptions("#buzz-content > div > div.feed-cards > article > div:nth-child(3) > div >p")

        self._set_posts_and_desc(posts_text, posts_link, posts_desc=posts_desc)



class TheNewYorkTimes(Source):
    """
    BuzzFeed content management and parsing
    """
    _home_uri = 'https://www.nytimes.com'
    _tech_uri = 'https://www.nytimes.com/section/technology'



    def  _parse_for_tech(self):
        posts_text = list(self._get_titles("#collection-highlights-container>div>ol>li>article>div>h2>a")
        + self._get_titles("#collection-technology>div:nth-child(2)>section:nth-child(3)>ol>li>article>div>h2>a"))
        
        posts_relative_link = list(self._get_links("#collection-highlights-container>div>ol>li>article>div>h2>a")
        + self._get_links("#collection-technology>div:nth-child(2)>section:nth-child(3)>ol>li>article>div>h2>a"))
        
        posts_desc = list(self._get_descriptions("#collection-highlights-container>div>ol>li>article>div>p.css-1jhf0lz")
        + self._get_descriptions("#collection-technology>div:nth-child(2)>section:nth-child(3)>ol>li>article>div>p:nth-child(2)"))

        self._set_posts_and_desc(posts_text, posts_relative_link, posts_desc=posts_desc, link_relative=True)



class TheNextWeb(Source):
    """
    BuzzFeed content management and parsing
    """
    _home_uri = 'https://thenextweb.com/'
    _tech_uri = 'https://thenextweb.com/neural'

    def _parse_for_home(self):
        posts_text = list(self._get_titles("h4.c-card__heading>a")
        + self._get_titles("section>div>ul>li>a"))
    
        posts_link = list(self._get_links("h4.c-card__heading>a")
        + self._get_links("section>div>ul>li>a"))        

        self._set_posts_and_desc(posts_text, posts_link, desc_available=False, link_relative=True)


    def  _parse_for_tech(self):
        # self._posts[self._soup.select("ul.c-coverStories>li>div>h2>a")[0].get_text().strip()] = self._soup.select("ul.c-coverStories>li>div>h2>a")[0]['href']
       
        posts_text = list(self._get_titles("h3.c-card__heading>a")
        + self._get_titles("div.c-articleList>article>div>h4>a"))
        
        # posts_link = list(self._get_links("ul.c-coverStories>li>div>h3>a")
        # + self._get_links("ul.c-posts>li>div:nth-child(1)>h3>a"))        
        posts_link = list(self._get_links("h3.c-card__heading>a")
        + self._get_links("div.c-articleList>article>div>h4>a"))        

        self._set_posts_and_desc(posts_text, posts_link, desc_available=False, link_relative=True)