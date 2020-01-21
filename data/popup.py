from tkinter import *
from data import const

def changeDimensionsPopup():
    window = Tk()

    window.title('Configure')

    prevRows = IntVar(window, value = const.noOfRows)
    rowsLabel = Label(window, text='Rows: ')
    rowsBox = Entry(window, textvariable = prevRows)
    prevCols = IntVar(window, value = const.noOfColumns)
    columnsLabel = Label(window, text='Columns: ')
    columnsBox = Entry(window, textvariable = prevCols)

    diagVal = IntVar(window, value = (const.noOfDirections == 8))
    diagCheckBox = Checkbutton(window, text='Use diagonals', variable=diagVal, onvalue = 1, offvalue = 0)

    def onsubmit():
        newCols = columnsBox.get()
        newRows = rowsBox.get()
        if newCols.isnumeric() and 5 <= int(newCols) <= 100 and newRows.isnumeric() and 5 <= int(newRows) <= 50:
            const.noOfColumns = int(newCols)
            const.noOfRows = int(newRows)

        if diagVal.get() == 1:
            const.setDirections(8)
        else:
            const.setDirections(4)

        window.quit()
        window.destroy()
        
    submit = Button(window, text='Change', command=onsubmit)

    submit.grid(columnspan=2, row=3, pady = 5)
    columnsLabel.grid(row=1, column = 0, pady=3, padx = 5)
    columnsBox.grid(row=1, column=1, pady=3, padx = 10)
    rowsLabel.grid(row=0, pady=3)
    rowsBox.grid(row=0, column=1, pady=3)
    diagCheckBox.grid(row = 2, columnspan = 2, pady = 5, padx = 5)
    
    window.columnconfigure(1, weight = 1)

     
    windowWidth = window.winfo_reqwidth()
    windowHeight = window.winfo_reqheight()

    # Gets both half the screen width/height and window width/height
    positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)

    # Positions the window in the center of the page.
    window.geometry("+{}+{}".format(positionRight, positionDown))

    window.attributes("-topmost", True)
    window.update()
    mainloop()