from bs4 import BeautifulSoup
import urllib.request
from class_Controller import *
import sys

class Scrapper :
    #c'tor 
    def __init__(self, pFirstPage, pGoalPage) : 
        self.Controller             = None
        self.__pages                = []
        self.__previousPagesTitle   = []
        self.__counter              = 0        
        self.__urlBeginning         = "https://fr.wikipedia.org"
        self.__goalPage             = pGoalPage
        self.currentPage            = pFirstPage
        self.__currentPageUrl       = None
        self.currentPageMainContent = None
        self.__pageTitle            = None
        self.__links                = None

    # private :

    # send error message to gui
    # @params : error message (str)
    # @return : None
    def __sendError(self, pErrorMsg) :
        self.Controller.sendError(pErrorMsg)

    # send page title to gui
    # @params : None
    # @return : None
    def __sendPageTitle(self) :
        self.Controller.sendPageTitle(self.__pageTitle)

    # open a random page as the goal, store its url to compare it every time player open a new page
    # in normal game, self.__goalPage is wikipedia's random url at entry and is set to goal page within the method
    # @params : None
    # @return : None
    def __getGoalPage(self) : 
        self.__goalPage = urllib.request.urlopen(self.__goalPage).geturl()
        self.__sendGoalPageTitle( self.getPageTitle( self.getPageMainContainer(self.__goalPage) ) )

    # send signal to UI to update goal title, method called once at the beginning of the game
    # @params : goal page title (str)
    # @return : None
    def __sendGoalPageTitle(self, pTitle) :
        self.Controller.sendGoalPageTitle(pTitle)

    # send previous page title to UI to show it within info at the bottom
    # @params : None
    # @return : None
    def __sendPreviousPageTitle(self) :
        self.Controller.sendPreviousPageTitle( self.__previousPagesTitle[ -1 ] )

    # send counter everytime a page is scrapped
    # @params : None
    # @return : None
    def __sendCounter(self) :
        self.Controller.sendCounter(self.__counter)

    # send signal to UI to finish the game, giving the counter
    # @params : None
    # @return : summary content (str) or nothing
    def __finishGame(self) :
        self.Controller.finishGame(self.__counter)

    # get content of the summary in the last scrapped page
    # @params : current page
    # @return : summary content (str)
    def __getPageSummary(self, pCurrentPageMainContainer) :
        for divTag in pCurrentPageMainContainer.findChildren("div", { "id" : "toc", "class" : "toc", "role" : "navigation" }) :
            return divTag.find_previous( "p" ).get_text()
            
    # send content of the summary in the last scrapped page, if that page has no summary
    # send a message to display "no summary"
    # @params : summary content (str)
    # @return : None
    def __sendSummary(self, pSummaryContent) :
        if ( pSummaryContent != None and len(pSummaryContent) > 0 ) :
            self.Controller.sendSummary(pSummaryContent)
        else :
            self.Controller.sendSummary("Pas de résumé pour cette page")

    # public : 

    def setController(self, pController) :
        self.Controller = pController

    # prime the scrapper, called once by controller
    def initScrapper(self) :        
        self.currentPageMainContent = self.getPageMainContainer(self.currentPage)
        self.__links                = self.getPageLinks(self.currentPageMainContent)
        self.__pageTitle            = self.getPageTitle(self.currentPageMainContent)
        self.__sendPageTitle()
        self.__sendSummary( self.__getPageSummary(self.currentPageMainContent) )
        self.__pages.append(self.__currentPageUrl)
        self.__getGoalPage()

    # getter for "links" dictionnary
    # @params : None
    # @return : links (collection)
    def getLinks(self) :
        return self.__links
    
    # used to get the main title of the page
    # also used to check if player found the page
    # @params : main div of the current page
    # @return : main title as string
    def getPageTitle(self, pMainDiv) : 
        return pMainDiv.findChildren("h1")[0].get_text()
        self.__pageTitle = self.currentPageMainContent.findChildren("h1")[0].get_text()
            
    # get all the <a> tags within the main content of the page
    # also sort them to get only those who can lead us to next page
    # @params : main div of the current page
    # @return : hashmap with link title as key and link as value
    def getPageLinks(self, pMainDiv) :
        lLinks = {}
        #iterator = 0
        for link in pMainDiv.findChildren("a") :
            if (link.find_parent( "span", { "class" : "mw-editsection" } ) ) :  #those links are used to modify pages content
                continue
            elif (link.find_parent( "span", { "class" : "plainlinks"} ) ) : #same as previous
                continue
            elif ( link.find_parent( "div", { "class" : "bandeau-cell" } ) ) : #some small articles contain a banner 
                continue
            elif ( link.get_text == "archive" ) : #we don't need those links
                continue
            elif ( link.get("href") == None ) :     #some links are hidden
                continue
            elif ( link.get("href")[0] == "#" ) :   #page anchor not needed
                continue
            elif ( link.find_parent("div", { "class" : "printfooter" } ) ) : #other hidden links
                continue
            elif ( link.get_text() == "" ) :    #some other hidden links
                continue
            elif ( link.has_attr("class") ) :   #external links
                continue
            else :
                #print("{}. id : {}, class : {}".format(iterator,link.get("id"), link.get("class")))
                lLinks[ link.get_text() ] = link.get("href")
            #iterator += 1
        
        return lLinks

    # get the main container of the wikipedia page
    # @params : url as string
    # @return : main div tag returned by beautifulSoup
    def getPageMainContainer(self, pUrl) :
        lPage                 = urllib.request.urlopen(pUrl)
        lSoupScrapping        = BeautifulSoup(lPage, "html.parser")
        lPageMainContent      = lSoupScrapping.find( "main", { "id" : "content" } )
        self.__currentPageUrl = lPage.geturl()
        print("page ouverte : {}, page recherchée : {}".format(lPage.geturl(), self.__goalPage))
        return lPageMainContent

    # concat standard beginning url for wikipedia with player's choosen page
    # ensure url for the next page is ok
    # @params : const url start, value from links hashmap
    # @return : formated url as string
    def formatUrl(self, pPage) :
        return self.__urlBeginning + pPage

    # store new page and scrap it
    # @params : new page title as string
    # @return : None
    def ScrapPage(self, pPageTitle) :
        self.__previousPagesTitle.append(self.__pageTitle)
        self.__sendPreviousPageTitle()
        self.currentPage            = self.formatUrl( self.__links[pPageTitle] )
        self.currentPageMainContent = self.getPageMainContainer(self.currentPage)
        self.__links                = self.getPageLinks(self.currentPageMainContent)
        self.__pageTitle            = self.getPageTitle(self.currentPageMainContent)
        self.__pages.append( self.__currentPageUrl )
        self.__sendPageTitle()
        self.__sendSummary( self.__getPageSummary(self.currentPageMainContent) )
        self.__counter += 1
        self.__sendCounter()
        if ( self.__currentPageUrl == self.__goalPage ) :
            self.__finishGame()   
    
    # scrap previous page
    # @params : new page title as string
    # @return : None
    def ScrapPreviousPage(self) :
        if ( len(self.__pages) <= 1 ) :
            self.__sendError("Pas de page précédentes")
        else :
            if ( len(self.__previousPagesTitle) > 1) :
                self.__previousPagesTitle.pop()
            self.__pages.pop()
            self.currentPageMainContent = self.getPageMainContainer(self.__pages[-1])
            self.__links                = self.getPageLinks(self.currentPageMainContent)   
            self.__pageTitle            = self.getPageTitle(self.currentPageMainContent)
            self.__sendPageTitle()
            self.__sendSummary( self.__getPageSummary(self.currentPageMainContent) )
            self.__sendPreviousPageTitle()
            self.__counter += 1
            self.__sendCounter()

    # get paragraph containing link focused in the gui's listbox to gui
    # params : link focused, act as a key for __links dictionnary
    # return : paragraph as a string
    def getParentParagraph(self, pLinkTitle) :
        for link in self.currentPageMainContent.findChildren("a") :
            if ( link.get_text() == pLinkTitle ) :
                return link.find_parent().find_parent().find_parent().get_text()
