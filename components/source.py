import bs4

class Source():
    """
    Base class for all content sources
    """
    def __init__(self,uri):
        self._uri = uri

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
        else:
            raise ValueError("Something went wrong with response received from "+resp.url+". Reson: "+resp.reason)

    def parse(self):
        raise NotImplementedError


class QuantaMagazine(Source):
    """
    QuantaMagazine content parsing and management
    """
    def parse(self):
        pass


class Reuters(Source):
    """
    Reuters content parsing and management
    """
    def parse(self):
        pass


class TechCrunch(Source):
    """
    TechCrunch content parsing and management
    """
    def parse(self):
        pass


class Wired(Source):
    """
    Wired content parsing and management
    """
    def parse(self):
        pass