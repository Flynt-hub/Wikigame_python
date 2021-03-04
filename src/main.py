from class_Controller import *
from class_GUI import *
from class_Scrapper import *

if __name__ == "__main__" :

    if len(sys.argv) > 1 :
        if sys.argv[1] == "debug" :
            firstPage = "https://fr.wikipedia.org/wiki/Python_(langage)"
            goalPage  = "https://fr.wikipedia.org/wiki/C_(langage)"
        else : 
            print("unknown argument..")
            sys.exit()
    else : 
        firstPage = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
        goalPage  = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"

    scrapper   = Scrapper( firstPage, goalPage )
    gui        = GUI("1400x800")
    controller = Controller( scrapper, gui )

    controller.Gui.root.mainloop()
