import tkinter as tk
import tkinter.font as font
from class_Controller import *

#class containing UI for wikigames, every widget is a private member configured and set by private method
#class c'tor need height and width for the window in string format like "(height)x(width)"
#c'tor also need a controller object to communicate with scrapper
class GUI : 
    #c'tor
    def __init__(self, pSize) : 
        self.__rootBg     = "#99ccff"
        self.__widgetsBg  = "#99ccff"
        self.__globalFont = "Ebrima"
        self.__titleFont  = None
        self.rootSize     = pSize

        self.__helpFilePath                = "../resources/help.txt"
        self.__bannerPath                  = "../images/Wikipedia_Banner.svg.png"
        self.__nextLinkButtonImagePath     = "../images/magnifyingGlass.png"
        self.__previousLinkButtonImagePath = "../images/previousButton2.png"

        self.Controller = None

        self.root                 = tk.Tk()
        self.__mainFrame          = tk.Frame(self.root)
        self.__bannerImage        = tk.PhotoImage()
        self.__bannerContainer    = tk.Label(self.__mainFrame)
        self.__linkListScroll     = tk.Scrollbar(self.__mainFrame)
        self.__linkList           = tk.Listbox(self.__mainFrame)
        self.__nextLinkImage      = tk.PhotoImage()
        self.__previousLinkImage  = tk.PhotoImage()
        self.__nextLinkButton     = tk.Button(self.__mainFrame)
        self.__previousLinkButton = tk.Button(self.__mainFrame)
        self.__infoContainer      = tk.Frame(self.__mainFrame)
        self.__paragraphContainer = tk.Frame(self.__mainFrame)

        self.__pageToFindTxt      = tk.Label(self.__infoContainer)
        self.__pageToFindValue    = tk.Label(self.__infoContainer)
        self.__countTxt           = tk.Label(self.__infoContainer)
        self.__countValue         = tk.Label(self.__infoContainer)
        self.__previousPageTxt    = tk.Label(self.__infoContainer)
        self.__previousPageValue  = tk.Label(self.__infoContainer)

        self.__paragraphTitle     = tk.Label(self.__paragraphContainer)
        self.__summary            = tk.Text(self.__paragraphContainer)
        self.__linkParagraph      = tk.Text(self.__paragraphContainer)
        self.__summaryScroll      = tk.Scrollbar(self.__paragraphContainer)
        self.__paragraphScroll    = tk.Scrollbar(self.__paragraphContainer)

        self.__menuBar            = tk.Menu(self.root)
        self.__menuFile           = tk.Menu(self.__menuBar)
        self.__menuStyle          = tk.Menu(self.__menuBar)
        self.__menuHelp           = tk.Menu(self.__menuBar)

    # private : 

    #all following methods are private and used to set up UI
    # no params and no return
    def __initRoot(self) : 
        self.root.geometry(self.rootSize)
        self.__titleFont = font.Font( size = 20, family = self.__globalFont )

    def __initMainFrame(self) :
        self.__mainFrame.configure( bg = self.__rootBg )
        self.__mainFrame.master.title("WIKIGAME")
        self.__mainFrame.pack( fill = tk.BOTH, expand = True )
        self.__mainFrame.columnconfigure( 0, weight = 1, pad = 7 )
        self.__mainFrame.rowconfigure( 1, weight = 1, pad = 7 )

    def __initMenus(self) :
        self.__menuFile.add_command( label = "Exit", command = self.root.quit )
        self.__menuStyle.add_command( label = "Dark mode", command = self.__switchColorMode )
        self.__menuHelp.add_command( label = "Help", command = self.__showHelp )

        self.__menuBar.add_cascade( label = "File", menu = self.__menuFile )
        self.__menuBar.add_cascade( label = "Style", menu = self.__menuStyle )
        self.__menuBar.add_cascade( label = "Help", menu = self.__menuHelp )

        self.root.config( menu = self.__menuBar )

    def __setBanner(self) : 
        self.__bannerImage.configure( file = self.__bannerPath )
        self.__bannerImage = self.__bannerImage.subsample(2)
        self.__bannerContainer.configure( image = self.__bannerImage)
        self.__bannerContainer.grid( row = 0, column = 0, columnspan = 4, sticky = "ns", padx = (5, 155), pady = (20, 5) )

    def __setParagraph(self) :
        self.__paragraphContainer['bg'] = self.__widgetsBg
        self.__paragraphContainer.grid( row = 1, column = 0, columnspan = 1, rowspan = 2, sticky = "news", padx = 5, pady = 5 )
        self.__paragraphContainer.rowconfigure( 1, weight = 4 )
        self.__paragraphContainer.rowconfigure( 2, weight = 2 )
        self.__paragraphContainer.columnconfigure( 2, weight = 2 )

        self.__paragraphTitle.configure( text = "titre du paragraphe", bg = self.__widgetsBg, font = self.__titleFont )
        self.__paragraphTitle['font'] = self.__titleFont
        self.__paragraphTitle.grid( row = 0, column = 0, columnspan = 3, sticky = "news", padx = 5, pady = 5 )
        self.__summary.configure( relief = tk.GROOVE, wrap = tk.WORD, state = tk.DISABLED, bg = self.__widgetsBg, font = self.__globalFont )
        self.__summary.grid( row = 1, column = 0, columnspan = 3, sticky = "new", pady = 5 )
        self.__linkParagraph.configure( relief = tk.GROOVE, wrap = tk.WORD, state = tk.DISABLED, bg = self.__widgetsBg, font = self.__globalFont )
        self.__linkParagraph.tag_configure("blue", foreground = "blue")
        self.__linkParagraph.grid( row = 2, column = 0, columnspan = 3, rowspan = 2 ,sticky = "news", pady = 5 )
        self.__summaryScroll.configure( command = self.__summary.yview )
        self.__summaryScroll.grid( row = 1, column = 3, sticky = "nes", pady = 5 )
        self.__paragraphScroll.configure( command = self.__linkParagraph.yview )
        self.__paragraphScroll.grid( row = 2, column = 3, rowspan = 2 ,sticky = "nes", pady = 5 )

    def __setLinkList(self) : 
        self.__linkListScroll.grid( row = 0, column = 4, rowspan = 2, sticky = "ns", pady = (20, 5) )        
        self.__linkList.configure(yscrollcommand = self.__linkListScroll.set, width = 40, relief = tk.FLAT, bg = self.__widgetsBg, font = self.__globalFont )
        self.__linkList.grid( row = 0, column = 2, columnspan = 2, rowspan = 2, sticky = "news", padx = 5, pady = (20, 5) )
        self.__linkListScroll.config(command = self.__linkList.yview)

    def __setNavigateButtons(self) : 
        self.__nextLinkImage.configure(file = self.__nextLinkButtonImagePath)
        self.__nextLinkImage = self.__nextLinkImage.subsample(2)

        self.__previousLinkImage.configure(file = self.__previousLinkButtonImagePath)
        self.__previousLinkImage = self.__previousLinkImage.subsample(2)

        self.__previousLinkButton.configure( image = self.__previousLinkImage, bg = self.__widgetsBg, borderwidth = 0, activebackground = self.__widgetsBg, command = self.__navigateToPreviousPage )
        self.__previousLinkButton.grid( row = 2, column = 2, columnspan = 1, sticky = "ns", padx = 5, pady = 5 )

        self.__nextLinkButton.configure( image = self.__nextLinkImage, bg = self.__widgetsBg, borderwidth = 0, activebackground = self.__widgetsBg, command = self.__navigateToNextPage )
        self.__nextLinkButton.grid( row = 2, column = 3, columnspan = 1, sticky = "ns", padx = 5, pady = 5 )

    def __setInfos(self) :
        self.__infoContainer.grid( row = 3, column = 0, columnspan = 6, sticky = "news", padx = 5, pady = (20, 20) )
        self.__infoContainer.columnconfigure( 16, weight = 2 )

        self.__pageToFindTxt.configure( text = "Page à trouver : ", anchor = "e", bg = self.__widgetsBg, font = self.__globalFont )
        self.__pageToFindValue.configure( text = "Une page bien planquée", anchor = "w", bg = self.__widgetsBg, font = self.__globalFont )
        self.__countTxt.configure( text = "Compteur : ", bg = self.__widgetsBg, font = self.__globalFont )
        self.__countValue.configure( text = "0", bg = self.__widgetsBg, font = self.__globalFont )
        self.__previousPageTxt.configure( text = "Page précédente : ", anchor = "e", bg = self.__widgetsBg, font = self.__globalFont )
        self.__previousPageValue.configure( text = "Une page avant celle-ci", anchor = "w", bg = self.__widgetsBg, font = self.__globalFont )

        self.__pageToFindTxt.pack( side = tk.LEFT, expand = tk.YES, fill = tk.X )
        self.__pageToFindValue.pack( side = tk.LEFT, expand = tk.YES, fill = tk.X, anchor = "w" )
        self.__countTxt.pack(side = tk.LEFT)
        self.__countValue.pack(side = tk.LEFT)
        self.__previousPageValue.pack(side = tk.RIGHT, expand = tk.YES, fill = tk.X )
        self.__previousPageTxt.pack( side = tk.RIGHT, expand = tk.YES, fill = tk.X )

    # method called by menu button, change colors of widgets
    # @params : None
    # @return : None
    def __switchColorMode(self) :
        self.__rootBg    = "#222222" if self.__rootBg == "#99ccff" else "#99ccff"
        self.__widgetsBg = "#444444" if self.__widgetsBg == "#99ccff" else "#99ccff"
        self.__menuStyle.entryconfigure(1, label = ( "Bright mode" if self.__menuStyle.entrycget(1, "label") == "Dark mode" else "Dark mode") )
        
        self.__mainFrame.configure( bg = self.__rootBg )
        self.__paragraphContainer.configure( bg = self.__widgetsBg )
        self.__linkParagraph.configure( bg = self.__widgetsBg )
        self.__summary.configure( bg = self.__widgetsBg )
        self.__paragraphTitle.configure( bg = self.__widgetsBg )
        self.__linkList.configure( bg = self.__widgetsBg )
        self.__previousLinkButton.configure( bg = self.__rootBg )
        self.__nextLinkButton.configure( bg = self.__rootBg )
        self.__pageToFindTxt.configure( bg = self.__rootBg )
        self.__pageToFindValue.configure( bg = self.__rootBg )
        self.__countTxt.configure( bg = self.__rootBg )
        self.__countValue.configure( bg = self.__rootBg )
        self.__previousPageTxt.configure( bg = self.__rootBg )
        self.__previousPageValue.configure( bg = self.__rootBg )

    # method called by menu button, show help in top window
    # @params : None
    # @return : None
    def __showHelp(self) :
        lHelpWindow = tk.Toplevel(self.root)
        lHelpWindow.geometry("500x400")
        lHelpWindow.title("Comment qu'on fait?")

        lHelpMsg    = tk.Message( lHelpWindow, text = self.__readHelpFile(), width = 500 )
        lHelpBtn    = tk.Button( lHelpWindow, text = "Fermer", command = lambda : self.__closeTopWindow(lHelpWindow), width = 200 )
        lHelpMsg.pack( expand = tk.YES, fill = tk.X )
        lHelpBtn.pack( expand = tk.YES, padx = 25 )

    # read external file 
    # @params : None
    # @return : external file content (str)
    def __readHelpFile(self) :
        lFilePointer = open( self.__helpFilePath, "r", encoding = "utf-8" )

        lSomeData = "this string is empty when the file is finished reading"
        lFileContent = ""

        while(lSomeData != "") :
            lSomeData = lFilePointer.readline()
            lFileContent += lSomeData
        lFilePointer.close()
        return lFileContent

    # method called by the "next" button, send signal throught controller to scrapper to scrap user's choosen page
    # @params : None
    # @return : None
    def __navigateToNextPage(self) : 
        try:
            self.Controller.ScrapNextPage( self.__linkList.get( self.__linkList.curselection() ), self.supplyList )
        except error:
            pass
    
    # method called by the "previous" button, send signal throught controller to scrapper to scrap previous page
    # @params : None
    # @return : None
    def __navigateToPreviousPage(self) :
        try:
            self.Controller.ScrapPreviousPage(self.supplyList)
        except expression as identifier:
            pass
    
    # automatically called when a link in the listBox is focused, send signal to scrapper to get parent's paragraph 
    # @params : fired event
    # @return : None
    def __getCorrespondingParagraph(self, event) :
        try:           
            lParagraph = self.Controller.getCorrespondingParagraph( self.__linkList.get( self.__linkList.curselection( ) ) )
            self.__supplyParagraph(lParagraph)  
            self.__highlightLinkInParagraph( self.__linkList.get( self.__linkList.curselection( ) ), "blue" )          
        except tk.TclError :
            pass # for unknown reason, event is catch when user highlight words in the Text widget.. This is not a critical error

    # fullfill paragraph label with selected link's parent's text
    # @params : parent's content as (long) string
    # @return : None
    def __supplyParagraph(self, pContent) :
        self.__linkParagraph.configure( state = tk.NORMAL)
        self.__linkParagraph.delete('1.0', tk.END)
        self.__linkParagraph.insert('1.0', pContent)
        self.__linkParagraph.configure( state = tk.DISABLED)

    # method to close the top window opened to show error
    # @params : top window to close
    # @return : None
    def __closeTopWindow(self, pTopWindow) :
        pTopWindow.destroy()
        pTopWindow.update()

    # when user click on a link, its parent text appear in the text widget, this method highlight this link in the text
    # @params : selected link (str), preconfigure tag (str), starting search from (float), until (float)
    # @return : None
    def __highlightLinkInParagraph( self, pLink, pTag, start = 1.0, end = "end" ) :
        start = self.__linkParagraph.index(start)
        end   = self.__linkParagraph.index(end)
        self.__linkParagraph.mark_set("matchStart", start)
        self.__linkParagraph.mark_set("matchEnd", start)
        self.__linkParagraph.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.__linkParagraph.search( pLink, "matchEnd", "searchLimit", count = count )
            if index == "": 
                break
            if count.get() == 0: 
                break 
            self.__linkParagraph.mark_set( "matchStart", index )
            self.__linkParagraph.mark_set("matchEnd", "%s+%sc" % ( index, count.get() ) )
            self.__linkParagraph.tag_add( pTag, "matchStart", "matchEnd" )

    # public : 

    def setController(self, pController) :
        self.Controller = pController

    # update summary widget with content sent by scrapper
    # @params : content (str)
    # @return : None
    def updateSummary(self, pContent) :
        self.__summary.configure( state = tk.NORMAL)
        self.__summary.delete('1.0', tk.END)
        self.__summary.insert('1.0', pContent)
        self.__summary.configure( state = tk.DISABLED)

    # method called by scrapper throught controller to show error in a top window
    # @params : error message (str)
    # @return : None
    def showError(self, pErrorMsg) :
        lErrorWindow = tk.Toplevel(self.root)
        lErrorWindow.geometry("200x100")
        lErrorWindow.title("Je crois qu'il y a un problème..")
        lErrorMsg    = tk.Message(lErrorWindow, text = pErrorMsg, width = 200)
        lErrorBtn    = tk.Button(lErrorWindow, text = "Fermer", command = lambda : self.__closeTopWindow(lErrorWindow) )
        lErrorMsg.pack(expand = tk.YES, fill = tk.X)
        lErrorBtn.pack(expand = tk.YES, fill = tk.X, padx = 25)

    # prime the UI, called once by controller
    # @params : None
    # @return : None
    def initUi(self) :
        self.__initRoot()
        self.__initMainFrame()
        self.__setBanner()
        self.__setParagraph()
        self.__setLinkList()
        self.__setNavigateButtons()
        self.__setInfos()
        self.__initMenus()
        self.__linkList.bind( "<<ListboxSelect>>", self.__getCorrespondingParagraph )

    # supply the listBox widget with the keys from the scrapper's links dictionnary
    # @params : scrapper link's list dictionnary
    # @return : None
    def supplyList(self, links) :
        self.__linkList.delete(0, tk.END)
        index = 0
        for key in links.keys() :
            self.__linkList.insert(index, key)
            index += 1

    # update title of the current page every time a link is open
    # @params : new page title (str)
    # @return : None
    def updateParagraphTitle(self, pPageTitle) :
        self.__paragraphTitle.configure( text = pPageTitle )

    # update counter every time a link is open or user go back to previous page
    # @params : counter from scrapper (int)
    # @return : None
    def updateCounter(self, pCounter) :
        self.__countValue.configure( text = pCounter )

    # open a top window to show a congratulation message with the counter
    # @params : counter from scrapper (int)
    # @return : None
    def finishGame(self, pCounter) :
        lWinWindow = tk.Toplevel(self.root)
        lWinWindow.geometry("300x300")
        lWinWindow.title("Fin de partie !!")

        lWinMsg     = tk.Message(lWinWindow, text = "Bravo! Vous avez terminer la partie", width = 200)
        lCounterMsg = tk.Message(lWinWindow, text = "Vous y etes parvenu en {} pages".format(pCounter), width = 200)
        lCloseBtn   = tk.Button(lWinWindow, text  = "Fermer", command = self.root.quit )

        lWinMsg.pack(expand = tk.YES, fill = tk.X)
        lCounterMsg.pack(expand = tk.YES, fill = tk.X)
        lCloseBtn.pack(expand = tk.YES, fill = tk.X, padx = 25)

    # update goal title, method called once at the beginning of the game
    # @params : goal page title (str)
    # @return : None
    def updateGoalPageTitle(self, pTitle) :
        self.__pageToFindValue.configure( text = pTitle )

    # update goal title, method called once at the beginning of the game
    # @params : previous page title (str)
    # @return : None
    def updatePreviousPageTitle(self, pPreviousPageTitle) :
        self.__previousPageValue.configure( text = pPreviousPageTitle)

