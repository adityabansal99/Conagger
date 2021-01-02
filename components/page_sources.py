from components import source


QUANTA_MAGAZINE = 'QuantaMagazine'
REUTERS = 'Reuters'
TECH_CRUNCH = 'TechCrunch'
WIRED = 'Wired'
BBC = 'BBC'
THE_VERGE = 'TheVerge'
BUZZFEED = 'BuzzFeed'
NY_TIMES = 'The New York Times'
TNW = 'The Next Web'


class Home():

    def __init__(self,sources):
        self._sources = self._instantiate_sources(sources)

    @property
    def sources(self):
        return self._sources


    @staticmethod
    def _instantiate_sources(content_sources):
        sources = []
        if QUANTA_MAGAZINE in content_sources:
            sources.append(source.QuantaMagazine.create_for_home(QUANTA_MAGAZINE))
        if REUTERS in content_sources:
            sources.append(source.Reuters.create_for_home(REUTERS))
        if TECH_CRUNCH in content_sources:
            sources.append(source.TechCrunch.create_for_home(TECH_CRUNCH))
        if WIRED in content_sources:
            sources.append(source.Wired.create_for_home(WIRED))
        if BBC in content_sources:
            sources.append(source.BBC.create_for_home(BBC))
        if THE_VERGE in content_sources:
            sources.append(source.TheVerge.create_for_home(THE_VERGE))
        return sources


class Science():

    def __init__(self,sources):
        self._sources = self._instantiate_sources(sources)

    @property
    def sources(self):
        return self._sources


    @staticmethod
    def _instantiate_sources(content_sources):
        sources = []
        if  QUANTA_MAGAZINE in content_sources:
            sources.append(source.QuantaMagazine.create_for_science(QUANTA_MAGAZINE))
        if REUTERS in content_sources:
            sources.append(source.Reuters.create_for_science(REUTERS))
        if THE_VERGE in content_sources:
            sources.append(source.TheVerge.create_for_science(THE_VERGE))
        return sources


class Tech():

    def __init__(self,sources):
        self._sources = self._instantiate_sources(sources)

    @property
    def sources(self):
        return self._sources


    @staticmethod
    def _instantiate_sources(content_sources):
        sources = []
        if BUZZFEED in content_sources:
            sources.append(source.BuzzFeed.create_for_tech(BUZZFEED))
        if REUTERS in content_sources:
            sources.append(source.Reuters.create_for_tech(REUTERS))
        if TECH_CRUNCH in content_sources:
            sources.append(source.TechCrunch.create_for_tech(TECH_CRUNCH))
        if NY_TIMES in content_sources:
            sources.append(source.TheNewYorkTimes.create_for_tech(NY_TIMES))
        if TNW in content_sources:
            sources.append(source.TheNextWeb.create_for_tech(TNW))
        if THE_VERGE in content_sources:
            sources.append(source.TheVerge.create_for_tech(THE_VERGE))
        return sources