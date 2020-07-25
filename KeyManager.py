from tkinter import *
import uuid
import datetime
import sqlite3 as lite
import io

class KeyManager: #Hlavní třída - program

    def __init__(self):
        self.WindowInicialization()
        self.WindowContent()

    def WindowInicialization(self):
        self.window = Tk()
        self.window.title("Evidence klíčů")
        self.window.iconbitmap("keyManagerKey.ico")

    def WindowContent(self):
        self.frame = 0 #Snímky
        self.mainFrameList = Menu(self.window) #Lišta
        self.mainFrameList.add_command(label="Správa klíčů", command=self.Keys)
        self.mainFrameList.add_command(label="Správa uživatelů", command=self.Users)
        self.mainFrameList.add_command(label="Správa dveří", command=self.Doors)
        self.mainFrameList.add_command(label="Správa půjčování", command=self.Borrowing)
        self.mainFrameList.add_command(label="Zbylá zobrazení", command=self.Prints)
        self.mainFrameList.add_command(label="Správa databáze", command=self.Database)

        self.window.config(menu = self.mainFrameList)
        self.Keys()

    def Keys(self): #Klíče
        self.deleteProcess()
        self.frame = 1
        self.window.geometry("750x470+100+100")

        self.keyCode = StringVar()
        self.keyCodeBorrowers = StringVar()
        self.destKeyCode = StringVar()
        self.destKeyLabelText = StringVar()

        self.keyLabel = Label(self.window, text="Přidání klíče do databáze", font=("Open Sans","15","bold"))
        self.keyLabel.grid(row=0,column=0,padx=20,pady=5,columnspan=2)

        self.keyCodeLabel = Label(self.window, text="Kód klíče: ", font=("Open Sans", "13", "bold"))
        self.keyCodeLabel.grid(row=1, column=0,padx=20, pady= 10)

        self.keyCodeEntry = Entry(self.window,textvariable = self.keyCode,font = ("Open Sans","13"))
        self.keyCodeEntry.grid(row=1, column=1,padx=20, pady= 10)

        self.addKeyButton = Button(self.window, command=self.addKey, width=20, height=2, fg="black", bg="#00c200",text="Přidat klíč", font=("Open Sans","10", "bold")) # Funkcionalita - metoda addKey()
        self.addKeyButton.grid(row=2, column=1,padx=20, pady= 10)

        self.keyBorLabel = Label(self.window, text="Zobrazení půjčujícího daného klíče", font=("Open Sans", "15", "bold"))
        self.keyBorLabel.grid(row=0, column=2, padx=20, pady=5, columnspan=2)

        self.keyCodeLabelBor = Label(self.window, text="Kód klíče: ", font=("Open Sans", "13", "bold"))
        self.keyCodeLabelBor.grid(row=1, column=2, padx=20, pady= 10)

        self.keyCodeBorrowEntry = Entry(self.window, textvariable=self.keyCodeBorrowers, font=("Open Sans", "13"))
        self.keyCodeBorrowEntry.grid(row=1, column=3, padx=20, pady= 10)

        self.keyCodeBorrowButton = Button(self.window, command=self.keyBorrowers, width=30, height=2, fg="black", bg="#00c200",text="Zobrazit půjčujícího daného klíče", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda keyBorrowers()
        self.keyCodeBorrowButton.grid(row=2, column=2,columnspan=2,padx=20, pady= 10)

        self.availKeyButton = Button(self.window, command=self.availKeys, width=30, height=2, fg="black", bg="#00c200",text="Zobrazit volné klíče", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda availKeys()
        self.availKeyButton.grid(row=5, column=2, columnspan=2, padx=20, pady=10)

        self.destkeyLabel = Label(self.window, text="Odstranění klíče z databáze", font=("Open Sans", "15", "bold"))
        self.destkeyLabel.grid(row=4, column=0, padx=20, pady=5, columnspan=2)

        self.destkeyCodeLabel = Label(self.window, text="Kód klíče: ", font=("Open Sans", "13", "bold"))
        self.destkeyCodeLabel.grid(row=5, column=0, padx=20, pady=10)

        self.destkeyCodeEntry = Entry(self.window, textvariable=self.destKeyCode, font=("Open Sans", "13"))
        self.destkeyCodeEntry.grid(row=5, column=1, padx=20, pady=10)

        self.destKeyButton = Button(self.window, command=self.destKey, width=20, height=2, fg="black", bg="#00c200", text="Odstranit klíč", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda destKey()
        self.destKeyButton.grid(row=6, column=1, padx=20, pady=10)

        self.availKeyLabel = Label(self.window, text="Zobrazení volných klíčů", font=("Open Sans","15","bold"))
        self.availKeyLabel.grid(row=4, column=2, columnspan=2, padx=20, pady=10)

        self.addKeyLabel = Label(self.window, font=("Open Sans", "11"))
        self.addKeyLabel.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

        self.destaKeyLabel = Label(self.window, font=("Open Sans", "11"))
        self.destaKeyLabel.grid(row=7, column=0, columnspan=2, padx=20, pady=10)

        self.availKeyLabelConfirm = Label(self.window, font=("Open Sans", "11"))
        self.availKeyLabelConfirm.grid(row=6, column=2, columnspan=2, padx=20, pady=10)

        self.borrowersKeyLabelConfirm = Label(self.window, font=("Open Sans", "11"))
        self.borrowersKeyLabelConfirm.grid(row=3, column=2, columnspan=2, padx=20, pady=10)

    def addKey(self): #Vytvoření nového klíče
        if self.keyCode.get()=="":
            try:
                self.addKeyLabel.destroy()
            except:
                pass
            self.addKeyLabel = Label(self.window, text="Prosím, vyplňte pole", font=("Open Sans", "11"))
            self.addKeyLabel.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
        else:
            try:
                self.addKeyLabel.destroy()
            except:
                pass
            self.mydb = lite.connect("keyManagerDB.db")
            self.cursor = self.mydb.cursor()
            self.cursor.execute("SELECT * FROM `door_key` WHERE Code='" + self.keyCode.get() + "'")
            self.inputControl = self.cursor.fetchall()
            self.mydb.close()
            if self.inputControl != []:
                self.addKeyLabel = Label(self.window, text="Tento kód klíče již existuje",
                                            font=("Open Sans", "11"))
                self.addKeyLabel.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
            else:
                try:
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursor = self.mydb.cursor()
                    self.keyuuid = uuid.uuid4().int
                    self.keyuuid = str(self.keyuuid)
                    self.keyuuidshort = self.keyuuid[0:9]
                    self.cursor.execute(
                        "INSERT INTO `door_key` (Door_Key_ID, Code) VALUES ('" + self.keyuuidshort + "', '" + self.keyCode.get() + "')")
                    self.addKeyLabel = Label(self.window, text="Požadavek proveden", font=("Open Sans", "11"))
                    self.addKeyLabel.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
                    self.mydb.commit()
                    self.mydb.close()

                except:
                    self.addKeyLabel = Label(self.window,
                                                text="Chyba - klíč nebyl úspěšně přidán do databáze,\n zkontrolujte, zda zadáváte vše správně",
                                                font=("Open Sans", "11"))
                    self.addKeyLabel.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

    def keyBorrowers(self): #Vypsání půjčujícího daného klíče
        if self.keyCodeBorrowers.get()=="":
            try:
                self.borrowersKeyLabelConfirm.destroy()
            except:
                pass
            self.borrowersKeyLabelConfirm = Label(self.window, text="Prosím, vyplňte pole", font=("Open Sans", "11"))
            self.borrowersKeyLabelConfirm.grid(row=3, column=2, columnspan=2, padx=20, pady=10)
        else:
            try:
                self.borrowersKeyLabelConfirm.destroy()
            except:
                pass
            try:

                self.mydb = lite.connect("keyManagerDB.db")
                self.cursor = self.mydb.cursor()
                self.cursor.execute("SELECT Door_Key_ID FROM `door_key` WHERE Code='" + self.keyCodeBorrowers.get() + "'")
                self.inputControlKeyBorrow = self.cursor.fetchall()
                self.inputControlKeyBorrowID = self.inputControlKeyBorrow[0][0]
                self.mydb.close()
                if self.inputControlKeyBorrow == []:
                    self.borrowersKeyLabelConfirm = Label(self.window, text="Tento kód klíče neexistuje",
                                                font=("Open Sans", "11"))
                    self.borrowersKeyLabelConfirm.grid(row=3, column=2, columnspan=2, padx=20, pady=10)
                else:
                    try:
                        self.mydb = lite.connect("keyManagerDB.db")
                        self.cursorb = self.mydb.cursor()
                        self.userIDsBorrow=[]
                        self.dateFroms=[]
                        self.borrowingStatusIDsBorrow=[]
                        self.userNamesBorrow = []
                        self.userSurnamesBorrow = []
                        self.cursorb.execute(
                            "SELECT User_User_ID, Date_From, Borrowing_Status_ID FROM `borrowing_status` WHERE Key_Key_ID='" + str(self.inputControlKeyBorrowID) + "'")
                        self.inputControlBorrowSelect = self.cursorb.fetchall()
                        for i in range(len(self.inputControlBorrowSelect)):
                            self.userIDsBorrow.append(self.inputControlBorrowSelect[i][0])
                            self.dateFroms.append(self.inputControlBorrowSelect[i][1])
                            self.borrowingStatusIDsBorrow.append(self.inputControlBorrowSelect[i][2])
                        self.mydb.close()

                        for y in range(len(self.userIDsBorrow)):
                            self.mydb = lite.connect("keyManagerDB.db")
                            self.cursorc = self.mydb.cursor()
                            self.cursorc.execute(
                                "SELECT Name, Surname FROM `user` WHERE User_ID='" + str(self.userIDsBorrow[y]) + "'")
                            self.inputControlBorrowUserNameSurname = self.cursorc.fetchall()
                            self.userNamesBorrow.append(self.inputControlBorrowUserNameSurname[0][0])
                            self.userSurnamesBorrow.append(self.inputControlBorrowUserNameSurname[0][1])
                            self.mydb.close()
                        self.borrowersKeyLabelConfirm = Label(self.window, text="Zobrazení provedeno",
                                                              font=("Open Sans", "11"))
                        self.borrowersKeyLabelConfirm.grid(row=3, column=2, columnspan=2, padx=20, pady=10)
                        self.borrowersKeyString = "Všechna půjčení existujících uživatelů ke klíči s kódem "+self.keyCodeBorrowers.get()+" a s ID "+str(self.inputControlKeyBorrowID)+":"
                        for z in range(len(self.userIDsBorrow)):
                            self.borrowersKeyString = self.borrowersKeyString + "\n\n -----------------Oddělovač půjčení-----------------\n\n Jméno uživatele: "+str(self.userNamesBorrow[z])+"\tPřijmení uživatele: "+str(self.userSurnamesBorrow[z])+"\tID uživatele: "+str(self.userIDsBorrow[z])+"\nPůjčeno od: "+str(self.dateFroms[z])+"\tID půjčení: "+str(self.borrowingStatusIDsBorrow[z])
                        self.top = Toplevel()
                        self.top.title("Půjčující daného klíče")
                        self.top.iconbitmap("keyManagerKey.ico")
                        self.borrowersKeyLabelTop = Label(self.top,
                                                              text=self.borrowersKeyString,
                                                              font=("Open Sans", "11", "bold"))
                        self.borrowersKeyLabelTop.pack()

                    except:
                        self.borrowersKeyLabelConfirm = Label(self.window,
                                                text="Chyba - zobrazení nebylo provedeno,\n zkontrolujte, zda zadáváte vše správně",
                                                font=("Open Sans", "11"))
                        self.borrowersKeyLabelConfirm.grid(row=3, column=2, columnspan=2, padx=20, pady=10)
            except:
                self.borrowersKeyLabelConfirm = Label(self.window,
                                                      text="Chyba - zobrazení nebylo provedeno,\n zkontrolujte, zda zadáváte vše správně",
                                                      font=("Open Sans", "11"))
                self.borrowersKeyLabelConfirm.grid(row=3, column=2, columnspan=2, padx=20, pady=10)

    def availKeys(self): #Vypsání volných klíčů
        try:
            try:
                self.availKeyLabelConfirm.destroy()
            except:
                pass
            self.mydb = lite.connect("keyManagerDB.db")
            self.cursor = self.mydb.cursor()
            self.keyAvailIDs=[]
            self.cursor.execute("SELECT k.Door_Key_ID, k.Code FROM `door_key` k, `borrowing_status` bs WHERE bs.Key_Key_ID=k.Door_Key_ID")
            self.inputControlAvailKeys = self.cursor.fetchall()
            for l in range(len(self.inputControlAvailKeys)):
                self.keyAvailIDs.append(self.inputControlAvailKeys[l][0])
            self.mydb.close()
            self.mydb = lite.connect("keyManagerDB.db")
            self.cursorb = self.mydb.cursor()
            self.cursorb.execute(
                "SELECT Door_Key_ID FROM `door_key`")
            self.inputControlAvailKeysAll = self.cursorb.fetchall()
            self.inputControlAvailKeysAllMatrix = []
            self.whatToDestroy = []
            for t in range(len(self.inputControlAvailKeysAll)):
                for u in range(len(self.inputControlAvailKeysAll[t])):
                    self.inputControlAvailKeysAllMatrix.append(self.inputControlAvailKeysAll[t][u])
            for n in range(len(self.keyAvailIDs)):
                for h in range(len(self.inputControlAvailKeysAllMatrix)):
                    if str(self.inputControlAvailKeysAllMatrix[h])==str(self.keyAvailIDs[n]):
                        self.whatToDestroy.append(self.inputControlAvailKeysAllMatrix[h])
            for q in range(len(self.whatToDestroy)):
                self.indexToDestroy = self.inputControlAvailKeysAllMatrix.index(self.whatToDestroy[q])
                del self.inputControlAvailKeysAllMatrix[self.indexToDestroy]
            self.mydb.close()
            self.keyCodesAvail = []
            for a in range(len(self.inputControlAvailKeysAllMatrix)):
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorc = self.mydb.cursor()
                self.cursorc.execute(
                    "SELECT Code FROM `door_key` WHERE Door_Key_ID='"+str(self.inputControlAvailKeysAllMatrix[a])+"'")
                self.inputControlAvailKeyy = self.cursorc.fetchall()
                self.keyCodesAvail.append(self.inputControlAvailKeyy[0][0])
                self.mydb.close()

            self.availKeysString = "Vypsání volných klíčů:"
            for b in range(len(self.keyCodesAvail)):
                self.availKeysString = self.availKeysString + "\nID klíče: "+str(self.inputControlAvailKeysAllMatrix[b])+", Kód klíče: "+str(self.keyCodesAvail[b])
            self.topAvailKeys = Toplevel()
            self.topAvailKeys.title("Volné klíče")
            self.topAvailKeys.iconbitmap("keyManagerKey.ico")
            self.availKeysTopLabel = Label(self.topAvailKeys, text=self.availKeysString, font=("Open Sans", "11", "bold"))
            self.availKeysTopLabel.pack()
            self.availKeyLabelConfirm = Label(self.window,
                                              text="Zobrazení provedeno",
                                              font=("Open Sans", "11"))
            self.availKeyLabelConfirm.grid(row=6, column=2, columnspan=2, padx=20, pady=10)
        except:
            self.availKeyLabelConfirm = Label(self.window, text="Chyba - nebylo možné vypsat volné klíče,\nje možné, že nejsou žádné volné klíče", font=("Open Sans", "11"))
            self.availKeyLabelConfirm.grid(row=6, column=2, columnspan=2, padx=20, pady=10)

    def destKey(self): #Vymazávání klíčů
        if self.destKeyCode.get()=="":
            try:
                self.destaKeyLabel.destroy()
            except:
                pass
            self.destaKeyLabel = Label(self.window, text="Prosím, vyplňte pole", font=("Open Sans", "11"))
            self.destaKeyLabel.grid(row=7, column=0, columnspan=2, padx=20, pady=10)
        else:
            try:
                try:
                    self.destaKeyLabel.destroy()
                except:
                    pass
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursor = self.mydb.cursor()
                self.cursor.execute("SELECT Door_Key_ID FROM `door_key` WHERE Code='" + self.destKeyCode.get() + "'")
                self.inputControlKeyDest = self.cursor.fetchall()
                self.inputControlKeyDestID = self.inputControlKeyDest[0][0]
                self.mydb.close()
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorb = self.mydb.cursor()
                self.cursorb.execute("DELETE FROM `door_key` WHERE Code='" + self.destKeyCode.get() + "'")
                self.mydb.commit()
                self.mydb.close()
                try:
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursorc = self.mydb.cursor()
                    self.cursorc.execute("DELETE FROM `key2door` WHERE Key_Key_ID='" + str(self.inputControlKeyDestID) + "'")
                    self.mydb.commit()
                    self.mydb.close()
                except:
                    pass
                try:
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursorc = self.mydb.cursor()
                    self.cursorc.execute(
                            "DELETE FROM `borrowing_status` WHERE Key_Key_ID='" + str(self.inputControlKeyDestID) + "'")
                    self.mydb.commit()
                    self.mydb.close()
                except:
                    pass
                self.destaKeyLabel = Label(self.window, text="Požadavek proveden", font=("Open Sans", "11"))
                self.destaKeyLabel.grid(row=7, column=0, columnspan=2, padx=20, pady=10)
            except:
                self.destaKeyLabel = Label(self.window, text="Chyba - klíč nebyl úspěšně odstraněn z databáze,\n zkontrolujte, zda zadáváte vše správně",
                                         font=("Open Sans", "11"))
                self.destaKeyLabel.grid(row=7, column=0, columnspan=2, padx=20, pady=10)

    def Doors(self): #Dveře
        self.deleteProcess()
        self.frame = 2
        self.window.geometry("760x575+100+100")

        self.doorCode = StringVar()
        self.keyToDoorCode = StringVar()
        self.doorToKeyCode = StringVar()
        self.doorAddConfirmText = StringVar()
        self.keyDoorAddConfirmText = StringVar()
        self.destdoorCode = StringVar()
        self.doorDestConfirmText = StringVar()
        self.doorToKeyCodeDest = StringVar()
        self.keyToDoorCodeDest = StringVar()

        self.doorLabel = Label(self.window, text="Přidání dveří do databáze", font=("Open Sans", "15", "bold"))
        self.doorLabel.grid(row=0, column=0, padx=20, pady=5, columnspan=2)

        self.doorCodeLabel = Label(self.window, text="Kód dveří: ", font=("Open Sans", "13", "bold"))
        self.doorCodeLabel.grid(row=1, column=0, padx=20, pady=10)

        self.doorCodeEntry = Entry(self.window, textvariable=self.doorCode, font=("Open Sans", "13"))
        self.doorCodeEntry.grid(row=1, column=1, padx=20, pady=10)

        self.addDoorButton = Button(self.window, command=self.addDoor, width=20, height=2, bg="#00c200", fg="black",text="Přidat dveře", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda addDoor()
        self.addDoorButton.grid(row=2, column=1, padx=20, pady=10)

        self.doorToKeyLabel = Label(self.window, text="Přiřazení klíče ke dveřím", font=("Open Sans", "15", "bold"))
        self.doorToKeyLabel.grid(row=0, column=2, padx=20, pady=5, columnspan=2)

        self.keyDoorCodeLabel = Label(self.window, text="Kód klíče: ", font=("Open Sans", "13", "bold"))
        self.keyDoorCodeLabel.grid(row=1, column=2, padx=20, pady=10)

        self.keyDoorCodeEntry = Entry(self.window, textvariable=self.keyToDoorCode, font=("Open Sans", "13"))
        self.keyDoorCodeEntry.grid(row=1, column=3, padx=20, pady=10)

        self.doorKeyCodeLabel = Label(self.window, text="Kód dveří: ", font=("Open Sans", "13", "bold"))
        self.doorKeyCodeLabel.grid(row=2, column=2, padx=20, pady=10)

        self.doorKeyCodeEntry = Entry(self.window, textvariable=self.doorToKeyCode, font=("Open Sans", "13"))
        self.doorKeyCodeEntry.grid(row=2, column=3, padx=20, pady=10)

        self.keyDoorCodeButton = Button(self.window, command=self.keyToDoor, bg="#00c200", width=30, height=2, fg="black", text="Přiřadit klíč ke dveřím", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda keyToDoor()
        self.keyDoorCodeButton.grid(row=3, column=2, columnspan=2, padx=20, pady=10)

        self.doorAddConfirm = Label(self.window, font=("Open Sans", "13")) # Funkcionalita - metoda addDoor()
        self.doorAddConfirm.grid(row=3, column=0, padx=20, pady=5, columnspan=2)

        self.keyDoorAddConfirm = Label(self.window,font=("Open Sans", "13"))  # Funkcionalita - metoda keyToDoor()
        self.keyDoorAddConfirm.grid(row=4, column=2, padx=20, pady=5, columnspan=2)

        self.destdoorLabel = Label(self.window, text="Odstranění dveří z databáze", font=("Open Sans", "15", "bold"))
        self.destdoorLabel.grid(row=4, column=0, padx=20, pady=5, columnspan=2)

        self.destdoorCodeLabel = Label(self.window, text="Kód dveří: ", font=("Open Sans", "13", "bold"))
        self.destdoorCodeLabel.grid(row=5, column=0, padx=20, pady=10)

        self.destdoorCodeEntry = Entry(self.window, textvariable=self.destdoorCode, font=("Open Sans", "13"))
        self.destdoorCodeEntry.grid(row=5, column=1, padx=20, pady=10)

        self.destDoorButton = Button(self.window, command=self.destDoor, width=20, height=2, fg="black", bg="#00c200", text="Odstranit dveře", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda destDoor()
        self.destDoorButton.grid(row=6, column=1, padx=20, pady=10)

        self.doorDestConfirm = Label(self.window, font=("Open Sans", "13"))  # Funkcionalita - metoda destDoor()
        self.doorDestConfirm.grid(row=7, column=0, padx=20, pady=5, columnspan=2)

        self.doorToKeyDestLabel = Label(self.window, text="Odpřiřazení klíče ode dveří", font=("Open Sans", "15", "bold"))
        self.doorToKeyDestLabel.grid(row=5, column=2, padx=20, pady=5, columnspan=2)

        self.keyDoorCodeDestLabel = Label(self.window, text="Kód klíče: ", font=("Open Sans", "13", "bold"))
        self.keyDoorCodeDestLabel.grid(row=6, column=2, padx=20, pady=10)

        self.keyDoorCodeDestEntry = Entry(self.window, textvariable=self.keyToDoorCodeDest, font=("Open Sans", "13"))
        self.keyDoorCodeDestEntry.grid(row=6, column=3, padx=20, pady=10)

        self.doorKeyCodeDestLabel = Label(self.window, text="Kód dveří: ", font=("Open Sans", "13", "bold"))
        self.doorKeyCodeDestLabel.grid(row=7, column=2, padx=20, pady=10)

        self.doorKeyCodeDestEntry = Entry(self.window, textvariable=self.doorToKeyCodeDest, font=("Open Sans", "13"))
        self.doorKeyCodeDestEntry.grid(row=7, column=3, padx=20, pady=10)

        self.keyDoorCodeDestButton = Button(self.window, command=self.keyToDoorDest, width=30, height=2, fg="black", bg="#00c200",
                                        text="Odpřiřadit klíč ode dveří", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda keyToDoorDest()
        self.keyDoorCodeDestButton.grid(row=8, column=2, columnspan=2, padx=20, pady=10)

        self.keyDoorDestConfirm = Label(self.window, font=("Open Sans", "13"))  # Funkcionalita - metoda keyToDoorDest()
        self.keyDoorDestConfirm.grid(row=9, column=2, padx=20, pady=5, columnspan=2)

    def addDoor(self): #Přidávání dveří
        if self.doorCode.get()=="":
            try:
                self.doorAddConfirm.destroy()
            except:
                pass
            self.doorAddConfirm = Label(self.window, text="Prosím, vyplňte pole", font=("Open Sans", "11"))
            self.doorAddConfirm.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
        else:
            try:
                self.doorAddConfirm.destroy()
            except:
                pass
            self.mydb = lite.connect("keyManagerDB.db")
            self.cursor = self.mydb.cursor()
            self.cursor.execute("SELECT * FROM `door` WHERE Code='" + self.doorCode.get() + "'")
            self.inputControl = self.cursor.fetchall()
            self.mydb.close()
            if self.inputControl != []:
                self.doorAddConfirm = Label(self.window, text="Tento kód dveří již existuje",
                                            font=("Open Sans", "11"))
                self.doorAddConfirm.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
            else:
                try:
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursor = self.mydb.cursor()
                    self.dooruuid = uuid.uuid4().int
                    self.dooruuid = str(self.dooruuid)
                    self.dooruuidshort = self.dooruuid[0:9]
                    self.cursor.execute(
                        "INSERT INTO `door` (Door_ID, Code) VALUES ('" + self.dooruuidshort + "', '" + self.doorCode.get() + "')")
                    self.doorAddConfirm = Label(self.window, text="Požadavek proveden", font=("Open Sans", "11"))
                    self.doorAddConfirm.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
                    self.mydb.commit()
                    self.mydb.close()

                except:
                    self.doorAddConfirm = Label(self.window,
                                                text="Chyba - dveře nebyly úspěšně přidány do databáze,\n zkontrolujte, zda zadáváte vše správně",
                                                font=("Open Sans", "11"))
                    self.doorAddConfirm.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

    def keyToDoor(self): #Přiřazování klíčů ke dveřím
        if self.keyToDoorCode.get()=="" or self.doorToKeyCode.get()=="":
            try:
                self.keyDoorAddConfirm.destroy()
            except:
                pass
            self.keyDoorAddConfirm = Label(self.window, text="Prosím, vyplňte obě pole", font=("Open Sans", "11"))
            self.keyDoorAddConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)
        else:
            try:
                self.keyDoorAddConfirm.destroy()
            except:
                pass
            try:
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursor = self.mydb.cursor()
                self.cursor.execute("SELECT Door_Key_ID FROM `door_key` WHERE Code='" + self.keyToDoorCode.get() + "'")
                self.inputControlKey = self.cursor.fetchall()
                self.inputControlKeyID = self.inputControlKey[0][0]
                self.mydb.close()
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorb = self.mydb.cursor()
                self.cursorb.execute("SELECT Door_ID FROM `door` WHERE Code='" + self.doorToKeyCode.get() + "'")
                self.inputControlDoor = self.cursorb.fetchall()
                self.inputControlDoorID = self.inputControlDoor[0][0]
                self.mydb.close()
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorc = self.mydb.cursor()
                self.cursorc.execute("SELECT * FROM `key2door` WHERE Key_Key_ID='" + str(self.inputControlKeyID) + "' AND Door_Door_ID='"+str(self.inputControlDoorID)+"'")
                self.inputControlKey2Door = self.cursorc.fetchall()
                self.mydb.close()
                if self.inputControlKey2Door != []:
                    self.keyDoorAddConfirm = Label(self.window, text="Tento klíč již je k těmto dveřím přiřazen", font=("Open Sans", "11"))
                    self.keyDoorAddConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)
                else:
                    try:
                        self.mydb = lite.connect("keyManagerDB.db")
                        self.cursord = self.mydb.cursor()
                        self.key2dooruuid = uuid.uuid4().int
                        self.key2dooruuid = str(self.key2dooruuid)
                        self.key2dooruuidshort = self.key2dooruuid[0:9]
                        self.cursord.execute(
                            "INSERT INTO `key2door` (Key_Key_ID, Door_Door_ID, Key2Door_ID) VALUES ('" + str(self.inputControlKeyID) + "', '" + str(self.inputControlDoorID) + "', '" + self.key2dooruuidshort + "')")
                        self.keyDoorAddConfirm = Label(self.window, text="Požadavek proveden", font=("Open Sans", "11"))
                        self.keyDoorAddConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)
                        self.mydb.commit()
                        self.mydb.close()

                    except:
                        self.keyDoorAddConfirm = Label(self.window,
                                                text="Chyba - tento klíč se nepodařilo přiřadit k těmto\n dveřím, zkontrolujte, zda zadáváte vše správně",
                                                font=("Open Sans", "11"))
                        self.keyDoorAddConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)

            except:
                self.keyDoorAddConfirm = Label(self.window,
                                       text="Chyba - tento klíč se nepodařilo přiřadit k těmto\n dveřím, zkontrolujte, zda zadáváte vše správně",
                                       font=("Open Sans", "11"))
                self.keyDoorAddConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)

    def keyToDoorDest(self): #Odpřiřazování klíče ode dveří
        if self.keyToDoorCodeDest.get()=="" or self.doorToKeyCodeDest.get()=="":
            try:
                self.keyDoorDestConfirm.destroy()
            except:
                pass
            self.keyDoorDestConfirm = Label(self.window, text="Prosím, vyplňte obě pole", font=("Open Sans", "11"))
            self.keyDoorDestConfirm.grid(row=9, column=2, columnspan=2, padx=20, pady=10)
        else:
            try:
                self.keyDoorDestConfirm.destroy()
            except:
                pass
            try:
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursor = self.mydb.cursor()
                self.cursor.execute("SELECT Door_Key_ID FROM `door_key` WHERE Code='" + self.keyToDoorCodeDest.get() + "'")
                self.inputControlKey = self.cursor.fetchall()
                self.inputControlKeyID = self.inputControlKey[0][0]
                self.mydb.close()
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorb = self.mydb.cursor()
                self.cursorb.execute("SELECT Door_ID FROM `door` WHERE Code='" + self.doorToKeyCodeDest.get() + "'")
                self.inputControlDoor = self.cursorb.fetchall()
                self.inputControlDoorID = self.inputControlDoor[0][0]
                self.mydb.close()
                try:
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursorg = self.mydb.cursor()
                    self.cursorg.execute(
                            "DELETE FROM `key2door` WHERE Key_Key_ID = '"+str(self.inputControlKeyID)+"' AND Door_Door_ID = '"+str(self.inputControlDoorID)+"'")
                    self.keyDoorDestConfirm = Label(self.window, text="Požadavek proveden", font=("Open Sans", "11"))
                    self.keyDoorDestConfirm.grid(row=9, column=2, columnspan=2, padx=20, pady=10)
                    self.mydb.commit()
                    self.mydb.close()
                except:
                    self.keyDoorDestConfirm = Label(self.window,
                                                text="Chyba - nebylo možné odpřiřadit klíč,\nzkontrolujte, zda zadáváte vše správně",
                                               font=("Open Sans", "11"))
                    self.keyDoorDestConfirm.grid(row=9, column=2, columnspan=2, padx=20, pady=10)
            except:
                self.keyDoorDestConfirm = Label(self.window,
                                                text="Chyba - nebylo možné odpřiřadit klíč,\nzkontrolujte, zda zadáváte vše správně",
                                                font=("Open Sans", "11"))
                self.keyDoorDestConfirm.grid(row=9, column=2, columnspan=2, padx=20, pady=10)

    def destDoor(self): #Vymazávání dveří
        if self.destdoorCode.get()=="":
            try:
                self.doorDestConfirm.destroy()
            except:
                pass
            self.doorDestConfirm = Label(self.window, text="Prosím, vyplňte pole", font=("Open Sans", "11"))
            self.doorDestConfirm.grid(row=7, column=0, columnspan=2, padx=20, pady=10)

        else:
            try:
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursor = self.mydb.cursor()
                self.cursor.execute("SELECT Door_ID FROM `door` WHERE Code='" + self.destdoorCode.get() + "'")
                self.inputControlDoorDest = self.cursor.fetchall()
                self.inputControlDoorDestID = self.inputControlDoorDest[0][0]
                self.mydb.close()
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorb = self.mydb.cursor()
                self.cursorb.execute("DELETE FROM `door` WHERE Code='" + self.destdoorCode.get() + "'")
                self.mydb.commit()
                self.mydb.close()
                try:
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursorc = self.mydb.cursor()
                    self.cursorc.execute(
                        "DELETE FROM `key2door` WHERE Door_Door_ID='" + str(self.inputControlDoorDestID) + "'")
                    self.mydb.commit()
                    self.mydb.close()
                except:
                    pass
                self.doorDestConfirm = Label(self.window, text="Požadavek proveden", font=("Open Sans", "11"))
                self.doorDestConfirm.grid(row=7, column=0, columnspan=2, padx=20, pady=10)
            except:
                self.doorDestConfirm = Label(self.window, text="Chyba - dveře nebyly úspěšně odstraněny z databáze,\n zkontrolujte, zda zadáváte vše správně",font=("Open Sans", "11"))
                self.doorDestConfirm.grid(row=7, column=0, columnspan=2, padx=20, pady=10)

    def Users(self): #Půjčující
        self.deleteProcess()
        self.frame = 3
        self.window.geometry("850x520+100+100")

        self.userName = StringVar()
        self.userSurname = StringVar()
        self.userAddConfirmText = StringVar()
        self.userNameBorrowedText = StringVar()
        self.userSurnameBorrowedText = StringVar()
        self.userDestConfirmText = StringVar()
        self.destUserSurname = StringVar()
        self.destUserName = StringVar()

        self.userLabel = Label(self.window, text="Přidání uživatele do databáze", font=("Open Sans","15","bold"))
        self.userLabel.grid(row=0,column=0,padx=20,pady=5,columnspan=2)

        self.userNameLabel = Label(self.window, text="Jméno uživatele: ", font=("Open Sans", "13", "bold"))
        self.userNameLabel.grid(row=1, column=0,padx=20, pady= 10)

        self.userNameEntry = Entry(self.window,textvariable = self.userName,font = ("Open Sans","13"))
        self.userNameEntry.grid(row=1, column=1,padx=20, pady= 10)

        self.userSurnameLabel = Label(self.window, text="Přijmení uživatele: ", font=("Open Sans", "13", "bold"))
        self.userSurnameLabel.grid(row=2, column=0, padx=20, pady=10)

        self.userSurnameEntry = Entry(self.window, textvariable=self.userSurname, font=("Open Sans", "13"))
        self.userSurnameEntry.grid(row=2, column=1, padx=20, pady=10)

        self.addUserButton = Button(self.window, command=self.addUser, width=20, height=2, fg="black", bg="#00c200",text="Přidat uživatele", font=("Open Sans","10", "bold")) # Funkcionalita - metoda addUser()
        self.addUserButton.grid(row=3, column=1,padx=20, pady= 10)

        self.userAddConfirm = Label(self.window, font=("Open Sans", "13"))
        self.userAddConfirm.grid(row=4, column=0, padx=20, pady=10, columnspan=2)

        self.userBorLabel = Label(self.window, text="Zobrazení klíčů půjčených uživatelem", font=("Open Sans", "15", "bold"))
        self.userBorLabel.grid(row=0, column=2, padx=20, pady=5, columnspan=2)

        self.userNameLabelBor = Label(self.window, text="Jméno uživatele: ", font=("Open Sans", "13", "bold"))
        self.userNameLabelBor.grid(row=1, column=2, padx=20, pady=10)

        self.userNameBorrowEntry = Entry(self.window, textvariable=self.userNameBorrowedText, font=("Open Sans", "13"))
        self.userNameBorrowEntry.grid(row=1, column=3, padx=20, pady=10)

        self.userSurnameLabelBor = Label(self.window, text="Přijmení uživatele: ", font=("Open Sans", "13", "bold"))
        self.userSurnameLabelBor.grid(row=2, column=2, padx=20, pady=10)

        self.userSurnameBorrowEntry = Entry(self.window, textvariable=self.userSurnameBorrowedText, font=("Open Sans", "13"))
        self.userSurnameBorrowEntry.grid(row=2, column=3, padx=20, pady=10)

        self.userBorrowButton = Button(self.window, command=self.userBorrowed, width=30, height=2, fg="black", bg="#00c200",text="Zobrazit klíče půjčené uživatelem", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda userBorrowed()
        self.userBorrowButton.grid(row=3, column=2, columnspan=2, padx=20, pady=10)

        self.destuserLabel = Label(self.window, text="Odstranění uživatele z databáze", font=("Open Sans", "15", "bold"))
        self.destuserLabel.grid(row=5, column=0, padx=20, pady=5, columnspan=2)

        self.destuserNameLabel = Label(self.window, text="Jméno uživatele: ", font=("Open Sans", "13", "bold"))
        self.destuserNameLabel.grid(row=6, column=0, padx=20, pady=10)

        self.destuserNameEntry = Entry(self.window, textvariable=self.destUserName, font=("Open Sans", "13"))
        self.destuserNameEntry.grid(row=6, column=1, padx=20, pady=10)

        self.destuserSurnameLabel = Label(self.window, text="Přijmení uživatele: ", font=("Open Sans", "13", "bold"))
        self.destuserSurnameLabel.grid(row=7, column=0, padx=20, pady=10)

        self.destuserSurnameEntry = Entry(self.window, textvariable=self.destUserSurname, font=("Open Sans", "13"))
        self.destuserSurnameEntry.grid(row=7, column=1, padx=20, pady=10)

        self.destUserButton = Button(self.window, command=self.destUser, width=20, height=2, fg="black", bg="#00c200", text="Odstranit uživatele", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda destUser()
        self.destUserButton.grid(row=8, column=1, padx=20, pady=10)

        self.userDestConfirm = Label(self.window, font=("Open Sans", "13"))
        self.userDestConfirm.grid(row=9, column=0, padx=20, pady=10, columnspan=2)

        self.userBorrowConfirm = Label(self.window, font=("Open Sans", "13"))
        self.userBorrowConfirm.grid(row=4, column=2, padx=20, pady=10, columnspan=2)

    def addUser(self): #Přidávání uživatelů
        if self.userName.get()=="" or self.userSurname.get()=="":
            try:
                self.userAddConfirm.destroy()
            except:
                pass
            self.userAddConfirm = Label(self.window, text="Prosím, vyplňte obě pole", font=("Open Sans", "11"))
            self.userAddConfirm.grid(row=4, column=0, columnspan=2, padx=20, pady=10)
        else:
            try:
                self.userAddConfirm.destroy()
            except:
                pass
            self.mydb = lite.connect("keyManagerDB.db")
            self.cursor = self.mydb.cursor()
            self.cursor.execute("SELECT * FROM `user` WHERE Name='"+self.userName.get()+"' AND Surname='"+self.userSurname.get()+"'")
            self.inputControl = self.cursor.fetchall()
            self.mydb.close()
            if self.inputControl != []:
                self.userAddConfirm = Label(self.window, text="Toto jméno a přijmení již existuje, prosím,\n přidejte znak, kterým se budou jmenovci odlišovat",
                                            font=("Open Sans", "11"))
                self.userAddConfirm.grid(row=4, column=0, columnspan=2, padx=20, pady=10)
            else:
                try:
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursor = self.mydb.cursor()
                    self.useruuid = uuid.uuid4().int
                    self.useruuid = str(self.useruuid)
                    self.useruuidshort = self.useruuid[0:9]
                    self.cursor.execute(
                        "INSERT INTO `user` (User_ID, Name, Surname) VALUES ('" + self.useruuidshort + "', '" + self.userName.get() + "', '"+self.userSurname.get()+"')")
                    self.userAddConfirm = Label(self.window, text="Požadavek proveden", font=("Open Sans", "11"))
                    self.userAddConfirm.grid(row=4, column=0, columnspan=2, padx=20, pady=10)
                    self.mydb.commit()
                    self.mydb.close()

                except:
                    self.userAddConfirm = Label(self.window,
                                                text="Chyba - uživatel nebyl úspěšně přidán do databáze,\nzkontrolujte, zda zadáváte vše správně",
                                                font=("Open Sans", "11"))
                    self.userAddConfirm.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

    def userBorrowed(self): #Zobrazení klíčů půjčených uživatelem
        if self.userNameBorrowedText.get()=="" and self.userSurnameBorrowedText.get()=="":
            try:
                self.userBorrowConfirm.destroy()
            except:
                pass
            self.userBorrowConfirm = Label(self.window, text="Prosím, vyplňte obě pole", font=("Open Sans", "11"))
            self.userBorrowConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)
        else:
            try:
                self.userBorrowConfirm.destroy()
            except:
                pass
            try:
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursor = self.mydb.cursor()
                self.cursor.execute("SELECT User_ID FROM `user` WHERE Name='" + self.userNameBorrowedText.get() + "' AND Surname='"+self.userSurnameBorrowedText.get()+"'")
                self.inputControlUserBorrow = self.cursor.fetchall()
                self.inputControlUserBorrowID = self.inputControlUserBorrow[0][0]
                self.mydb.close()
                if self.inputControlUserBorrow == []:
                    self.userBorrowConfirm = Label(self.window, text="Tento uživatel neexistuje",
                                                font=("Open Sans", "11"))
                    self.userBorrowConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)
                else:
                    try:
                        self.mydb = lite.connect("keyManagerDB.db")
                        self.cursorb = self.mydb.cursor()
                        self.keyIDsBorrow=[]
                        self.dateFroms=[]
                        self.borrowingStatusIDsBorrow=[]
                        self.keyCodesBorrow = []
                        self.cursorb.execute(
                            "SELECT Key_Key_ID, Date_From, Borrowing_Status_ID FROM `borrowing_status` WHERE User_User_ID='" + str(self.inputControlUserBorrowID) + "'")
                        self.inputControlBorrowSelect = self.cursorb.fetchall()
                        for i in range(len(self.inputControlBorrowSelect)):
                            self.keyIDsBorrow.append(self.inputControlBorrowSelect[i][0])
                            self.dateFroms.append(self.inputControlBorrowSelect[i][1])
                            self.borrowingStatusIDsBorrow.append(self.inputControlBorrowSelect[i][2])
                        self.mydb.close()

                        for y in range(len(self.borrowingStatusIDsBorrow)):
                            self.mydb = lite.connect("keyManagerDB.db")
                            self.cursorc = self.mydb.cursor()
                            self.cursorc.execute(
                                "SELECT Code FROM `door_key` WHERE Door_Key_ID='" + str(self.keyIDsBorrow[y]) + "'")
                            self.inputControlBorrowKeyCode = self.cursorc.fetchall()
                            self.keyCodesBorrow.append(self.inputControlBorrowKeyCode[0][0])
                            self.mydb.close()
                        self.userBorrowConfirm = Label(self.window, text="Zobrazení provedeno",
                                                      font=("Open Sans", "11"))
                        self.userBorrowConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)
                        self.userBorrowedString = "Všechna půjčení klíčů uživatelem jménem "+self.userNameBorrowedText.get()+" "+self.userSurnameBorrowedText.get()+" a s ID "+str(self.inputControlUserBorrowID)+":"
                        for z in range(len(self.borrowingStatusIDsBorrow)):
                            self.userBorrowedString = self.userBorrowedString + "\n\n -----------------Oddělovač půjčení-----------------\n\n Kód klíče: "+str(self.keyCodesBorrow[z])+"\tID klíče: "+str(self.keyIDsBorrow[z])+"\nPůjčeno od: "+str(self.dateFroms[z])+"\tID půjčení: "+str(self.borrowingStatusIDsBorrow[z])
                        self.topp = Toplevel()
                        self.topp.title("Klíče půjčené uživatelem")
                        self.topp.iconbitmap("keyManagerKey.ico")
                        self.userBorrowedLabelTop = Label(self.topp,
                                                              text=self.userBorrowedString,
                                                              font=("Open Sans", "11", "bold"))
                        self.userBorrowedLabelTop.pack()

                    except:
                        self.userBorrowConfirm = Label(self.window,
                                                text="Chyba - zobrazení nebylo provedeno,\n zkontrolujte, zda zadáváte vše správně",
                                                font=("Open Sans", "11"))
                        self.userBorrowConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)
            except:
                self.userBorrowConfirm = Label(self.window,
                                                      text="Chyba - zobrazení nebylo provedeno,\n zkontrolujte, zda zadáváte vše správně",
                                                      font=("Open Sans", "11"))
                self.userBorrowConfirm.grid(row=4, column=2, columnspan=2, padx=20, pady=10)

    def destUser(self): #Vymazávání uživatelů
        if self.destUserName.get()=="" or self.destUserSurname.get()=="":
            try:
                self.userDestConfirm.destroy()
            except:
                pass
            self.userDestConfirm = Label(self.window, text="Prosím, vyplňte obě pole", font=("Open Sans", "11"))
            self.userDestConfirm.grid(row=9, column=0, columnspan=2, padx=20, pady=10)

        else:
            try:
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursor = self.mydb.cursor()
                self.cursor.execute("SELECT User_ID FROM `user` WHERE Name='" + self.destUserName.get() + "' AND Surname='"+self.destUserSurname.get()+"'")
                self.inputControlUserDest = self.cursor.fetchall()
                self.inputControlUserDestID = self.inputControlUserDest[0][0]
                self.mydb.close()
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorb = self.mydb.cursor()
                self.cursorb.execute("DELETE FROM `user` WHERE Name='" + self.destUserName.get() + "' AND Surname='"+self.destUserSurname.get()+"'")
                self.mydb.commit()
                self.mydb.close()
                try:
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursorc = self.mydb.cursor()
                    self.cursorc.execute(
                        "DELETE FROM `borrowing_status` WHERE User_User_ID='" + str(self.inputControlUserDestID) + "'")
                    self.mydb.commit()
                    self.mydb.close()
                except:
                    pass
                self.userDestConfirm = Label(self.window, text="Požadavek proveden",font=("Open Sans", "11"))
                self.userDestConfirm.grid(row=9, column=0, columnspan=2, padx=20, pady=10)
            except:
                self.userDestConfirm = Label(self.window, text="Chyba - uživatel nebyl úspěšně odstraněn z databáze,\nzkontrolujte, zda zadáváte vše správně",font=("Open Sans", "11"))
                self.userDestConfirm.grid(row=9, column=0, columnspan=2, padx=20, pady=10)

    def Borrowing(self): #Půjčení
        self.deleteProcess()
        self.frame = 4
        self.window.geometry("850x400+100+100")

        self.borrowKeyEntryText = StringVar()
        self.borrowNameEntryText = StringVar()
        self.borrowSurnameEntryText = StringVar()
        self.borrowEndSurnameEntryText = StringVar()
        self.borrowEndNameEntryText = StringVar()
        self.borrowEndKeyEntryText = StringVar()

        self.borrowLabel = Label(self.window, text="Vytvoření půjčení klíče", font=("Open Sans", "15", "bold"))
        self.borrowLabel.grid(row=0, column=0, padx=20, pady=5, columnspan=2)

        self.borrowEndLabel = Label(self.window, text="Ukončení půjčení klíče", font=("Open Sans", "15", "bold"))
        self.borrowEndLabel.grid(row=0, column=2, padx=20, pady=5, columnspan=2)

        self.borrowKeyLabel = Label(self.window, text="Kód klíče: ", font=("Open Sans", "13", "bold"))
        self.borrowKeyLabel.grid(row=1, column=0, padx=20, pady=10)

        self.borrowKeyEntry = Entry(self.window, textvariable=self.borrowKeyEntryText, font=("Open Sans", "13"))
        self.borrowKeyEntry.grid(row=1, column=1, padx=20, pady=10)

        self.borrowUserNameLabel = Label(self.window, text="Jméno uživatele: ", font=("Open Sans", "13", "bold"))
        self.borrowUserNameLabel.grid(row=2, column=0, padx=20, pady=10)

        self.borrowUserNameEntry = Entry(self.window, textvariable=self.borrowNameEntryText, font=("Open Sans", "13"))
        self.borrowUserNameEntry.grid(row=2, column=1, padx=20, pady=10)

        self.borrowUserSurnameLabel = Label(self.window, text="Přijmení uživatele: ", font=("Open Sans", "13", "bold"))
        self.borrowUserSurnameLabel.grid(row=3, column=0, padx=20, pady=10)

        self.borrowUserSurnameEntry = Entry(self.window, textvariable=self.borrowSurnameEntryText, font=("Open Sans", "13"))
        self.borrowUserSurnameEntry.grid(row=3, column=1, padx=20, pady=10)

        self.borrowStartButton = Button(self.window, command=self.borrowStart, width=30, height=2, fg="black", bg="#00c200", text="Vytvořit půjčení klíče", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda borrowStart()
        self.borrowStartButton.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

        self.borrowStartConfirm = Label(self.window, font=("Open Sans", "13"))
        self.borrowStartConfirm.grid(row=5, column=0, padx=20, pady=10, columnspan=2)

        self.borrowEndKeyLabel = Label(self.window, text="Kód klíče: ", font=("Open Sans", "13", "bold"))
        self.borrowEndKeyLabel.grid(row=1, column=2, padx=20, pady=10)

        self.borrowEndKeyEntry = Entry(self.window, textvariable=self.borrowEndKeyEntryText, font=("Open Sans", "13"))
        self.borrowEndKeyEntry.grid(row=1, column=3, padx=20, pady=10)

        self.borrowEndUserNameLabel = Label(self.window, text="Jméno uživatele: ", font=("Open Sans", "13", "bold"))
        self.borrowEndUserNameLabel.grid(row=2, column=2, padx=20, pady=10)

        self.borrowEndUserNameEntry = Entry(self.window, textvariable=self.borrowEndNameEntryText, font=("Open Sans", "13"))
        self.borrowEndUserNameEntry.grid(row=2, column=3, padx=20, pady=10)

        self.borrowEndUserSurnameLabel = Label(self.window, text="Přijmení uživatele: ", font=("Open Sans", "13", "bold"))
        self.borrowEndUserSurnameLabel.grid(row=3, column=2, padx=20, pady=10)

        self.borrowEndUserSurnameEntry = Entry(self.window, textvariable=self.borrowEndSurnameEntryText, font=("Open Sans", "13"))
        self.borrowEndUserSurnameEntry.grid(row=3, column=3, padx=20, pady=10)

        self.borrowEndButton = Button(self.window, command=self.borrowEnd, width=30, height=2, fg="black", bg="#00c200", text="Ukončit půjčení klíče", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda borrowEnd()
        self.borrowEndButton.grid(row=4, column=2, columnspan=2, padx=20, pady=10)

        self.borrowEndConfirm = Label(self.window, font=("Open Sans", "13"))
        self.borrowEndConfirm.grid(row=5, column=2, padx=20, pady=10, columnspan=2)

    def borrowStart(self): #Vytváření půjčení
        if self.borrowKeyEntryText.get()=="" or self.borrowNameEntryText.get()=="" or self.borrowSurnameEntryText.get()=="":
            try:
                self.borrowStartConfirm.destroy()
            except:
                pass
            self.borrowStartConfirm = Label(self.window, text="Prosím, vyplňte všechna pole", font=("Open Sans", "11"))
            self.borrowStartConfirm.grid(row=5, column=0, columnspan=2, padx=20, pady=10)
        else:
            try:
                self.borrowStartConfirm.destroy()
            except:
                pass
            try:
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursor = self.mydb.cursor()
                self.cursor.execute("SELECT Door_Key_ID FROM `door_key` WHERE Code='"+self.borrowKeyEntryText.get()+"'")
                self.inputControl = self.cursor.fetchall()
                self.inputControlKeyID = self.inputControl[0][0]
                self.mydb.close()
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursoru = self.mydb.cursor()
                self.cursoru.execute("SELECT User_ID FROM `user` WHERE Name='" + self.borrowNameEntryText.get() + "' AND Surname='"+self.borrowSurnameEntryText.get()+"'")
                self.inputControlUser = self.cursoru.fetchall()
                self.inputControlUserID = self.inputControlUser[0][0]
                self.mydb.close()
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorb = self.mydb.cursor()
                self.cursorb.execute("SELECT * FROM `borrowing_status` WHERE Key_Key_ID='" + str(self.inputControlKeyID) + "'")
                self.inputControlReal = self.cursorb.fetchall()
                self.mydb.close()
                if self.inputControlReal != []:
                    self.borrowStartConfirm = Label(self.window, text="Tento klíč již je půjčen, prosím, vraťte jej,\n než si ho bude moci půjčit další uživatel",
                                                font=("Open Sans", "11"))
                    self.borrowStartConfirm.grid(row=5, column=0, columnspan=2, padx=20, pady=10)
                else:
                    try:
                        self.mydb = lite.connect("keyManagerDB.db")
                        self.cursor = self.mydb.cursor()
                        self.borrowuuid = uuid.uuid4().int
                        self.borrowuuid = str(self.borrowuuid)
                        self.borrowuuidshort = self.borrowuuid[0:9]
                        self.borrowStarttime = datetime.datetime.now()
                        self.borrowStarttimeFinal = self.borrowStarttime.strftime('%Y-%m-%d %H:%M:%S')
                        self.cursor.execute(
                            "INSERT INTO `borrowing_status` (User_User_ID, Key_Key_ID, Date_From, Borrowing_Status_ID) VALUES ('" + str(self.inputControlUserID) + "', '" + str(self.inputControlKeyID) + "', '"+self.borrowStarttimeFinal+"', '"+self.borrowuuidshort+"' )")
                        self.borrowStartConfirm = Label(self.window, text="Požadavek proveden", font=("Open Sans", "11"))
                        self.borrowStartConfirm.grid(row=5, column=0, columnspan=2, padx=20, pady=10)
                        self.mydb.commit()
                        self.mydb.close()
                        with open("Borrowings.txt",mode="a",encoding="UTF-16")as self.file:
                            self.zapisStart = "\n\nZahájení půjčení\n\nJméno uživatele: "+self.borrowNameEntryText.get()+"\t Přijmení uživatele: "+self.borrowSurnameEntryText.get()+"\t ID uživatele: "+str(self.inputControlUserID)+"\nKód klíče: "+self.borrowKeyEntryText.get()+"\t ID klíče: "+str(self.inputControlKeyID)+"\nDoba půjčení: "+self.borrowStarttimeFinal+"\t ID půjčení: "+self.borrowuuidshort
                            self.file.write(self.zapisStart)
                            self.file.close()

                    except:
                        self.borrowStartConfirm = Label(self.window,
                                                    text="Chyba - půjčení nebylo možné vytvořit,\nzkontrolujte, zda zadáváte půjčujícího správně",
                                                    font=("Open Sans", "11"))
                        self.borrowStartConfirm.grid(row=5, column=0, columnspan=2, padx=20, pady=10)
            except:
                self.borrowStartConfirm = Label(self.window,
                                                text="Chyba - půjčení nebylo možné vytvořit,\nzkontrolujte, zda zadáváte půjčujícího a klíč správně",
                                                font=("Open Sans", "11"))
                self.borrowStartConfirm.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

    def borrowEnd(self): #Ukončování půjčení
        if self.borrowEndSurnameEntryText.get()=="" or self.borrowEndNameEntryText.get()=="" or self.borrowEndKeyEntryText.get()=="":
            try:
                self.borrowEndConfirm.destroy()
            except:
                pass
            self.borrowEndConfirm = Label(self.window, text="Prosím, vyplňte všechna pole", font=("Open Sans", "11"))
            self.borrowEndConfirm.grid(row=5, column=2, columnspan=2, padx=20, pady=10)
        else:
            try:
                self.borrowEndConfirm.destroy()
            except:
                pass
            try:
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursor = self.mydb.cursor()
                self.cursor.execute("SELECT Door_Key_ID FROM `door_key` WHERE Code='"+self.borrowEndKeyEntryText.get()+"'")
                self.inputControl = self.cursor.fetchall()
                self.inputControlKeyID = self.inputControl[0][0]
                self.mydb.close()
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursoru = self.mydb.cursor()
                self.cursoru.execute("SELECT User_ID FROM `user` WHERE Name='" + self.borrowEndNameEntryText.get() + "' AND Surname='"+self.borrowEndSurnameEntryText.get()+"'")
                self.inputControlUser = self.cursoru.fetchall()
                self.inputControlUserID = self.inputControlUser[0][0]
                self.mydb.close()
                try:
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursorg = self.mydb.cursor()
                    self.cursorg.execute(
                        "SELECT Borrowing_Status_ID FROM `borrowing_status` WHERE Key_Key_ID = '" + str(
                            self.inputControlKeyID) + "' AND User_User_ID = '" + str(self.inputControlUserID) + "'")
                    self.inputControlEndBorrowingID = self.cursorg.fetchall()
                    self.inputControlEndBorrowingIDFinal = self.inputControlEndBorrowingID[0][0]
                    self.mydb.close()
                    self.mydb = lite.connect("keyManagerDB.db")
                    self.cursor = self.mydb.cursor()
                    self.borrowEndtime = datetime.datetime.now()
                    self.borrowEndtimeFinal = self.borrowEndtime.strftime('%Y-%m-%d %H:%M:%S')
                    self.cursor.execute(
                        "DELETE FROM `borrowing_status` WHERE Key_Key_ID = '"+str(self.inputControlKeyID)+"' AND User_User_ID = '"+str(self.inputControlUserID)+"'")
                    self.borrowEndConfirm = Label(self.window, text="Požadavek proveden", font=("Open Sans", "11"))
                    self.borrowEndConfirm.grid(row=5, column=2, columnspan=2, padx=20, pady=10)
                    self.mydb.commit()
                    self.mydb.close()
                    with open("Borrowings.txt", mode="a", encoding="UTF-16")as self.file:
                        self.zapisEnd = "\n\nUkončení půjčení\n\nJméno uživatele: " + self.borrowEndNameEntryText.get() + "\t Přijmení uživatele: " + self.borrowEndSurnameEntryText.get() + "\t ID uživatele: " + str(
                            self.inputControlUserID) + "\nKód klíče: " + self.borrowEndKeyEntryText.get() + "\t ID klíče: " + str(
                            self.inputControlKeyID) + "\nDoba ukončení půjčení: " + self.borrowEndtimeFinal + "\t ID půjčení: " + str(self.inputControlEndBorrowingIDFinal)
                        self.file.write(self.zapisEnd)
                        self.file.close()

                except:
                    self.borrowEndConfirm = Label(self.window,
                                                text="Chyba - půjčení nebylo možné ukončit,\nzkontrolujte, zda zadáváte půjčujícího správně",
                                               font=("Open Sans", "11"))
                    self.borrowEndConfirm.grid(row=5, column=2, columnspan=2, padx=20, pady=10)
            except:
                self.borrowEndConfirm = Label(self.window,
                                                text="Chyba - půjčení nebylo možné ukončit,\nzkontrolujte, zda zadáváte půjčujícího a klíč správně",
                                                font=("Open Sans", "11"))
                self.borrowEndConfirm.grid(row=5, column=2, columnspan=2, padx=20, pady=10)

    def Database(self): #Databáze
        self.deleteProcess()
        self.frame = 5
        self.window.geometry("620x250+100+100")

        self.databasesBackupConfirmText = StringVar()
        self.databasesLoadConfirmText = StringVar()

        self.databaseBackupLabel = Label(self.window, text="Záloha databáze na disk", font=("Open Sans", "15", "bold"))
        self.databaseBackupLabel.grid(row=0, column=0, padx=20, pady=5, columnspan=2)

        self.databaseLoadLabel = Label(self.window, text="Načtení databáze ze zálohy", font=("Open Sans", "15", "bold"))
        self.databaseLoadLabel.grid(row=0, column=2, padx=20, pady=5, columnspan=2)

        self.databaseBackupButton = Button(self.window, command=self.databaseBackup, width=30, height=2, fg="black", bg="#00c200", text="Zálohovat databázi na disk", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda databaseBackup()
        self.databaseBackupButton.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        self.databaseLoadButton = Button(self.window, command=self.databaseLoad, width=30, height=2, fg="black", bg="#00c200", text="Načíst databázi ze zálohy", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda databaseLoad()
        self.databaseLoadButton.grid(row=1, column=2, columnspan=2, padx=20, pady=10)

        self.databaseBackupConfirmLabel = Label(self.window, font=("Open Sans", "13"))
        self.databaseBackupConfirmLabel.grid(row=2, column=0, padx=20, pady=5, columnspan=2)

        self.databaseLoadConfirmLabel = Label(self.window, font=("Open Sans", "13"))
        self.databaseLoadConfirmLabel.grid(row=2, column=2, padx=20, pady=5, columnspan=2)

    def databaseBackup(self): #Záloha databáze
        try:
            self.mydb = lite.connect("keyManagerDB.db")
            with io.open("backupKeyManagerDB.sql","w") as file:
                for linha in self.mydb.iterdump():
                    file.write("%s\n" % linha)
            self.databaseBackupConfirmLabel = Label(self.window, text="Záloha provedena", font=("Open Sans", "13"))
            self.databaseBackupConfirmLabel.grid(row=2, column=0, padx=20, pady=5, columnspan=2)
            self.mydb.close()
        except:
            self.databaseBackupConfirmLabel = Label(self.window,text="Chyba - záloha neprovedena", font=("Open Sans", "13"))
            self.databaseBackupConfirmLabel.grid(row=2, column=0, padx=20, pady=5, columnspan=2)

    def databaseLoad(self): #Načtení databáze
        try:
            self.mydb = lite.connect("keyManagerDB.db")

            self.loadFile = io.open("backupKeyManagerDB.sql","r")
            self.loadExecution = self.loadFile.readlines()
            self.cursor = self.mydb.cursor()
            for i in range(len(self.loadExecution)):
                self.cursor.execute(self.loadExecution[i])
            self.mydb.close()
            self.databaseLoadConfirmLabel = Label(self.window, text="Načtení databáze provedeno", font=("Open Sans", "13"))
            self.databaseLoadConfirmLabel.grid(row=2, column=2, padx=20, pady=5, columnspan=2)
        except:
            self.databaseLoadConfirmLabel = Label(self.window, text="Chyba - načtení databáze neprovedeno,\n nejspíše nemáte prázdnou databázi", font=("Open Sans", "13"))
            self.databaseLoadConfirmLabel.grid(row=2, column=2, padx=20, pady=5, columnspan=2)

    def Prints(self): #Výpisy
        self.deleteProcess()
        self.frame = 6
        self.window.geometry("660x310+100+100")

        self.printKeysLabel = Label(self.window, text="Zobrazení klíču", font=("Open Sans", "15", "bold"))
        self.printKeysLabel.grid(row=0, column=0, padx=20, pady=5, columnspan=2)

        self.printKeysButton = Button(self.window, command=self.printKeys, width=30, height=2, fg="black", bg="#00c200",text="Zobrazit klíče", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda printKeys()
        self.printKeysButton.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        self.printKeysConfirmLabel = Label(self.window, font=("Open Sans", "13"))
        self.printKeysConfirmLabel.grid(row=2, column=0, padx=20, pady=5, columnspan=2)

        self.printUsersLabel = Label(self.window, text="Zobrazení uživatelů", font=("Open Sans", "15", "bold"))
        self.printUsersLabel.grid(row=0, column=2, padx=20, pady=5, columnspan=2)

        self.printUsersButton = Button(self.window, command=self.printUsers, width=30, height=2, fg="black", bg="#00c200",text="Zobrazit uživatele", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda printUsers()
        self.printUsersButton.grid(row=1, column=2, columnspan=2, padx=20, pady=10)

        self.printUsersConfirmLabel = Label(self.window, font=("Open Sans", "13"))
        self.printUsersConfirmLabel.grid(row=2, column=2, padx=20, pady=5, columnspan=2)

        self.printDoorsLabel = Label(self.window, text="Zobrazení dveří", font=("Open Sans", "15", "bold"))
        self.printDoorsLabel.grid(row=3, column=0, padx=20, pady=5, columnspan=2)

        self.printDoorsButton = Button(self.window, command=self.printDoors, width=30, height=2, fg="black", bg="#00c200",text="Zobrazit dveře", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda printDoors()
        self.printDoorsButton.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

        self.printDoorsConfirmLabel = Label(self.window, font=("Open Sans", "13"))
        self.printDoorsConfirmLabel.grid(row=5, column=0, padx=20, pady=5, columnspan=2)

        self.printKey2DoorsLabel = Label(self.window, text="Zobrazení přiřazení klíčů ke dveřím", font=("Open Sans", "15", "bold"))
        self.printKey2DoorsLabel.grid(row=3, column=2, padx=20, pady=5, columnspan=2)

        self.printKey2DoorsButton = Button(self.window, command=self.printKey2Doors, width=30, height=2, fg="black", bg="#00c200",text="Zobrazit přiřazení klíčů ke dveřím", font=("Open Sans","10", "bold"))  # Funkcionalita - metoda printKey2Doors()
        self.printKey2DoorsButton.grid(row=4, column=2, columnspan=2, padx=20, pady=10)

        self.printKey2DoorsConfirmLabel = Label(self.window, font=("Open Sans", "13"))
        self.printKey2DoorsConfirmLabel.grid(row=5, column=2, padx=20, pady=5, columnspan=2)

    def printKeys(self): #Zobrazení existujících klíčů
        try:
            try:
                self.printKeysConfirmLabel.destroy()
            except:
                pass
            self.mydb = lite.connect("keyManagerDB.db")
            self.cursor = self.mydb.cursor()
            self.allKeysIDs = []
            self.allKeysCodes = []
            self.cursor.execute("SELECT Door_Key_ID, Code FROM `door_key`")
            self.inputControlKeys = self.cursor.fetchall()
            for l in range(len(self.inputControlKeys)):
                self.allKeysIDs.append(self.inputControlKeys[l][0])
                self.allKeysCodes.append(self.inputControlKeys[l][1])
            self.mydb.close()
            self.allKeysString = "Zobrazení klíčů:"
            for b in range(len(self.allKeysIDs)):
                self.allKeysString = self.allKeysString + "\nID klíče: "+str(self.allKeysIDs[b])+", Kód klíče: "+str(self.allKeysCodes[b])
            self.topAllKeys = Toplevel()
            self.topAllKeys.title("Existující klíče")
            self.topAllKeys.iconbitmap("keyManagerKey.ico")
            self.allKeysTopLabel = Label(self.topAllKeys, text=self.allKeysString, font=("Open Sans", "11", "bold"))
            self.allKeysTopLabel.pack()
            self.printKeysConfirmLabel = Label(self.window,
                                              text="Zobrazení provedeno",
                                              font=("Open Sans", "11"))
            self.printKeysConfirmLabel.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
        except:
            self.printKeysConfirmLabel = Label(self.window, text="Chyba - nebylo možné zobrazit klíče", font=("Open Sans", "11"))
            self.printKeysConfirmLabel.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

    def printUsers(self): #Zobrazení existujících uživatelů
        try:
            try:
                self.printUsersConfirmLabel.destroy()
            except:
                pass
            self.mydb = lite.connect("keyManagerDB.db")
            self.cursor = self.mydb.cursor()
            self.allUsersIDs = []
            self.allUsersNames = []
            self.allUsersSurnames = []
            self.cursor.execute("SELECT User_ID, Name, Surname FROM `user`")
            self.inputControlUsers = self.cursor.fetchall()
            for l in range(len(self.inputControlUsers)):
                self.allUsersIDs.append(self.inputControlUsers[l][0])
                self.allUsersNames.append(self.inputControlUsers[l][1])
                self.allUsersSurnames.append(self.inputControlUsers[l][2])
            self.mydb.close()
            self.allUsersString = "Zobrazení uživatelů:"
            for b in range(len(self.allUsersIDs)):
                self.allUsersString = self.allUsersString + "\nID uživatele: "+str(self.allUsersIDs[b])+", Jméno uživatele: "+str(self.allUsersNames[b])+", Přijmení uživatele: "+str(self.allUsersSurnames[b])
            self.topAllUsers = Toplevel()
            self.topAllUsers.title("Existující uživatelé")
            self.topAllUsers.iconbitmap("keyManagerKey.ico")
            self.allUsersTopLabel = Label(self.topAllUsers, text=self.allUsersString, font=("Open Sans", "11", "bold"))
            self.allUsersTopLabel.pack()
            self.printUsersConfirmLabel = Label(self.window,
                                              text="Zobrazení provedeno",
                                              font=("Open Sans", "11"))
            self.printUsersConfirmLabel.grid(row=2, column=2, columnspan=2, padx=20, pady=10)
        except:
            self.printUsersConfirmLabel = Label(self.window, text="Chyba - nebylo možné zobrazit uživatele", font=("Open Sans", "11"))
            self.printUsersConfirmLabel.grid(row=2, column=2, columnspan=2, padx=20, pady=10)

    def printDoors(self): #Zobrazení existujících dveří
        try:
            try:
                self.printDoorsConfirmLabel.destroy()
            except:
                pass
            self.mydb = lite.connect("keyManagerDB.db")
            self.cursor = self.mydb.cursor()
            self.allDoorsIDs = []
            self.allDoorsCodes = []
            self.cursor.execute("SELECT Door_ID, Code FROM `door`")
            self.inputControlDoors = self.cursor.fetchall()
            for l in range(len(self.inputControlDoors)):
                self.allDoorsIDs.append(self.inputControlDoors[l][0])
                self.allDoorsCodes.append(self.inputControlDoors[l][1])
            self.mydb.close()
            self.allDoorsString = "Zobrazení dveří:"
            for b in range(len(self.allDoorsIDs)):
                self.allDoorsString = self.allDoorsString + "\nID dveří: "+str(self.allDoorsIDs[b])+", Kód dveří: "+str(self.allDoorsCodes[b])
            self.topAllDoors = Toplevel()
            self.topAllDoors.title("Existující dveře")
            self.topAllDoors.iconbitmap("keyManagerKey.ico")
            self.allDoorsTopLabel = Label(self.topAllDoors, text=self.allDoorsString, font=("Open Sans", "11", "bold"))
            self.allDoorsTopLabel.pack()
            self.printDoorsConfirmLabel = Label(self.window,
                                              text="Zobrazení provedeno",
                                              font=("Open Sans", "11"))
            self.printDoorsConfirmLabel.grid(row=5, column=0, columnspan=2, padx=20, pady=10)
        except:
            self.printDoorsConfirmLabel = Label(self.window, text="Chyba - nebylo možné zobrazit dveře", font=("Open Sans", "11"))
            self.printDoorsConfirmLabel.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

    def printKey2Doors(self): #Zobrazení existujících Key2Door vztahů
        try:
            try:
                self.printKey2DoorsConfirmLabel.destroy()
            except:
                pass
            self.mydb = lite.connect("keyManagerDB.db")
            self.cursor = self.mydb.cursor()
            self.allKey2DoorIDs = []
            self.allKeyIDs = []
            self.allDoorIDs = []
            self.allKeyCodes = []
            self.allDoorCodes = []
            self.cursor.execute("SELECT Key2Door_ID, Key_Key_ID, Door_Door_ID FROM `key2door`")
            self.inputControlKeyDoors = self.cursor.fetchall()
            for l in range(len(self.inputControlKeyDoors)):
                self.allKey2DoorIDs.append(self.inputControlKeyDoors[l][0])
                self.allKeyIDs.append(self.inputControlKeyDoors[l][1])
                self.allDoorIDs.append(self.inputControlKeyDoors[l][2])
            self.mydb.close()
            for z in range(len(self.inputControlKeyDoors)):
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorb = self.mydb.cursor()
                self.cursorb.execute("SELECT Code FROM `door_key` WHERE Door_Key_ID='"+str(self.allKeyIDs[z])+"'")
                self.inputControlKeyCodes = self.cursorb.fetchall()
                self.allKeyCodes.append(self.inputControlKeyCodes[0][0])
                self.mydb.close()
            for y in range(len(self.inputControlKeyDoors)):
                self.mydb = lite.connect("keyManagerDB.db")
                self.cursorc = self.mydb.cursor()
                self.cursorc.execute("SELECT Code FROM `door` WHERE Door_ID='" + str(self.allDoorIDs[z]) + "'")
                self.inputControlDoorCodes = self.cursorc.fetchall()
                self.allDoorCodes.append(self.inputControlDoorCodes[0][0])
                self.mydb.close()
            self.allKey2DoorsString = "Zobrazení přiřazení klíčů ke dveřím:"
            for b in range(len(self.allKey2DoorIDs)):
                self.allKey2DoorsString = self.allKey2DoorsString + "\nID přiřazení: " + str(
                    self.allKey2DoorIDs[b]) + ", ID klíče: " + str(self.allKeyIDs[b])+", Kód klíče: "+str(self.allKeyCodes[b])+", ID dveří: "+str(self.allDoorIDs[b])+", Kód dveří: "+str(self.allDoorCodes[b])
            self.topAllKey2Doors = Toplevel()
            self.topAllKey2Doors.title("Existující přiřazení klíčů ke dveřím")
            self.topAllKey2Doors.iconbitmap("keyManagerKey.ico")
            self.allKey2DoorsTopLabel = Label(self.topAllKey2Doors, text=self.allKey2DoorsString, font=("Open Sans", "11", "bold"))
            self.allKey2DoorsTopLabel.pack()
            self.printKey2DoorsConfirmLabel = Label(self.window,
                                            text="Zobrazení provedeno",
                                            font=("Open Sans", "11"))
            self.printKey2DoorsConfirmLabel.grid(row=5, column=2, columnspan=2, padx=20, pady=10)

        except:
            self.printKey2DoorsConfirmLabel = Label(self.window, text="Chyba - nebylo možné\n zobrazit přiřazení klíčů ke dveřím", font=("Open Sans", "11"))
            self.printKey2DoorsConfirmLabel.grid(row=5, column=2, columnspan=2, padx=20, pady=10)

    def deleteProcess(self): #Mazání při překlikávání
        if self.frame==0:
            pass

        if self.frame==1: #Mazání framu "Správa klíčů"
            self.keyLabel.destroy()
            self.keyCodeLabel.destroy()
            self.keyCodeEntry.destroy()
            self.addKeyButton.destroy()
            self.keyBorLabel.destroy()
            self.keyCodeLabelBor.destroy()
            self.keyCodeBorrowEntry.destroy()
            self.keyCodeBorrowButton.destroy()
            self.addKeyLabel.destroy()
            self.availKeyButton.destroy()
            self.destkeyLabel.destroy()
            self.destkeyCodeLabel.destroy()
            self.destkeyCodeEntry.destroy()
            self.destKeyButton.destroy()
            self.destaKeyLabel.destroy()
            self.availKeyLabel.destroy()
            self.availKeyLabelConfirm.destroy()
            self.borrowersKeyLabelConfirm.destroy()
            self.frame=0

        elif self.frame==2: #Mazání framu "Správa dveří"
            self.doorLabel.destroy()
            self.doorCodeLabel.destroy()
            self.doorCodeEntry.destroy()
            self.addDoorButton.destroy()
            self.doorToKeyLabel.destroy()
            self.keyDoorCodeLabel.destroy()
            self.keyDoorCodeEntry.destroy()
            self.doorKeyCodeLabel.destroy()
            self.doorKeyCodeEntry.destroy()
            self.keyDoorCodeButton.destroy()
            self.doorAddConfirm.destroy()
            self.keyDoorAddConfirm.destroy()
            self.destdoorLabel.destroy()
            self.destdoorCodeLabel.destroy()
            self.destdoorCodeEntry.destroy()
            self.destDoorButton.destroy()
            self.doorDestConfirm.destroy()
            self.keyDoorDestConfirm.destroy()
            self.keyDoorCodeDestButton.destroy()
            self.doorKeyCodeDestEntry.destroy()
            self.doorKeyCodeDestLabel.destroy()
            self.keyDoorCodeDestEntry.destroy()
            self.doorToKeyDestLabel.destroy()
            self.keyDoorCodeDestLabel.destroy()
            self.frame=0

        elif self.frame==3: #Mazání framu "Správa uživatelů"
            self.userLabel.destroy()
            self.userNameLabel.destroy()
            self.userNameEntry.destroy()
            self.userSurnameLabel.destroy()
            self.userSurnameEntry.destroy()
            self.addUserButton.destroy()
            self.userAddConfirm.destroy()
            self.userBorLabel.destroy()
            self.userNameLabelBor.destroy()
            self.userNameBorrowEntry.destroy()
            self.userSurnameLabelBor.destroy()
            self.userSurnameBorrowEntry.destroy()
            self.userBorrowButton.destroy()
            self.destuserLabel.destroy()
            self.destuserNameLabel.destroy()
            self.destuserNameEntry.destroy()
            self.destuserSurnameLabel.destroy()
            self.destuserSurnameEntry.destroy()
            self.destUserButton.destroy()
            self.userDestConfirm.destroy()
            self.userBorrowConfirm.destroy()
            self.frame=0

        elif self.frame==4: #Mazání framu "Správa půjčování"
            self.borrowLabel.destroy()
            self.borrowEndLabel.destroy()
            self.borrowKeyLabel.destroy()
            self.borrowKeyEntry.destroy()
            self.borrowUserNameLabel.destroy()
            self.borrowUserNameEntry.destroy()
            self.borrowUserSurnameLabel.destroy()
            self.borrowUserSurnameEntry.destroy()
            self.borrowStartButton.destroy()
            self.borrowStartConfirm.destroy()
            self.borrowEndKeyLabel.destroy()
            self.borrowEndKeyEntry.destroy()
            self.borrowEndUserNameLabel.destroy()
            self.borrowEndUserNameEntry.destroy()
            self.borrowEndUserSurnameLabel.destroy()
            self.borrowEndUserSurnameEntry.destroy()
            self.borrowEndButton.destroy()
            self.borrowEndConfirm.destroy()
            self.frame=0

        elif self.frame==5: #Mazání framu "Správa databáze"
            self.databaseBackupLabel.destroy()
            self.databaseLoadLabel.destroy()
            self.databaseBackupButton.destroy()
            self.databaseLoadButton.destroy()
            self.databaseBackupConfirmLabel.destroy()
            self.databaseLoadConfirmLabel.destroy()
            self.frame=0

        elif self.frame==6: #Mazání framu "Zbylá zobrazení"
            self.printKeysLabel.destroy()
            self.printKeysButton.destroy()
            self.printKeysConfirmLabel.destroy()
            self.printUsersLabel.destroy()
            self.printUsersButton.destroy()
            self.printUsersConfirmLabel.destroy()
            self.printDoorsLabel.destroy()
            self.printDoorsButton.destroy()
            self.printDoorsConfirmLabel.destroy()
            self.printKey2DoorsLabel.destroy()
            self.printKey2DoorsButton.destroy()
            self.printKey2DoorsConfirmLabel.destroy()
            self.frame=0

KeyManager() #Volání programu - hlavní třídy
mainloop() #Chod UI - Tkinter