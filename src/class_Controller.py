from class_GUI import *
from class_Scrapper import *

class Controller : 
    #c'tor
    def __init__(self, pScrapper, pGui) :
        self.Scrapper = pScrapper
        self.Gui      = pGui

        self.Scrapper.setController(self)
        self.Gui.setController(self)

        self.Gui.initUi()
        self.Scrapper.initScrapper()

        self.Gui.supplyList( self.Scrapper.getLinks() )

    # method called by "next" button from UI, relay signal to scrapper
    # @params : page title as string, method to call when scrapping is finish
    # @return : None
    def ScrapNextPage(self, pPageTitle, _pCallBack) :
        self.Scrapper.ScrapPage(pPageTitle)
        if _pCallBack :
            _pCallBack( self.Scrapper.getLinks() )

    # method called by "previous" button from UI, relay signal to scrapper
    # @params : method to call when scrapping is finish
    # @return : None
    def ScrapPreviousPage(self, _pCallBack) :
        self.Scrapper.ScrapPreviousPage()
        if _pCallBack :
            _pCallBack( self.Scrapper.getLinks() )

    # send paragraph containing link focused in the gui's listbox to UI
    # @params : selected link (str)
    # @return : paragraph content (str)
    def getCorrespondingParagraph(self, pLinkTitle) :
        return self.Scrapper.getParentParagraph(pLinkTitle)

    # send error message to UI
    # @params : error message (str)
    # @return : None
    def sendError(self, pErrorMsg) :
        self.Gui.showError(pErrorMsg)
    
    # send page title to UI
    # @params : page title (str)
    # @return : None
    def sendPageTitle(self, pPageTitle) :
        self.Gui.updateParagraphTitle(pPageTitle)

    # send page title to UI
    # @params : previous page title (str)
    # @return : None
    def sendPreviousPageTitle(self, pPreviousPageTitle) :
        self.Gui.updatePreviousPageTitle(pPreviousPageTitle)

    # send signal to UI to finish the game
    # @params : counter (int)
    # @return : None
    def finishGame(self, pCounter) :
        self.Gui.finishGame(pCounter)

    # send signal to UI to update goal page title
    # @params : goal page title (str)
    # @return : None
    def sendGoalPageTitle(self, pTitle) :
        self.Gui.updateGoalPageTitle(pTitle)

    # send signal to UI to update counter
    # @params : counter (int)
    # @return : None
    def sendCounter(self, pCounter) :
        self.Gui.updateCounter(pCounter)

    # send signal to UI to update summary
    # @params : summary content (str)
    # @return : None
    def sendSummary(self, pSummaryContent) :
        self.Gui.updateSummary(pSummaryContent)