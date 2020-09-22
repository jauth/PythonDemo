import time
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import csv

root = tk.Tk()

myfont = Font(family="Times New Roman", size=12)


FormatMoney = "${:0,.2f}"
PrintDivider = "---------------------------------------------------------------"
StoreDataFile = "Storedata.csv"
timesfont = ("Times New Roman", 11, "bold")

class StoreTimer:
    UpdateFreq = 100

    def __init__(self, store):
        self.Timer = store.Timer
        self.store = store
        self.TimerRunning = False

    def start_timer(self):
        if self.TimerRunning == False:
            self.TimerRunning = True
            self.starttime = time.time()
            root.after(StoreTimer.UpdateFreq, self.update_timer)  # root. because it needs to run off of root thread

    def update_timer(self):
        elapsed = time.time()-self.starttime
        if elapsed < self.Timer:
            self.store.progressbar["value"] = elapsed / self.Timer * 100
            root.after(StoreTimer.UpdateFreq, self.update_timer)
        else:
            self.TimerRunning = False
            self.store.progressbar["value"] = 0
            self.store.make_money()

            if self.store.ManagerUnlocked:
                self.start_timer()


class Store:
    Money = 5.00
    StoreList = []

    def __init__(self, storename, storeprofit, storecost, timer, managercost):
        self.StoreName = storename
        self.StoreCount = 0
        self.StoreProfit = float(storeprofit)
        self.StoreCost = float(storecost)
        self.Timer = float(timer)
        self.ManagerUnlocked = False
        self.ManagerCost = float(managercost)
        self.TimerObject = StoreTimer(self)
        self.clickbutton = None
        self.progressbar = None
        self.store_count_label = None
        self.store_cost_label = None
        self.buybutton = None
        self.manager_button = None

    @classmethod
    def display_stores(cls):
        tk.Label(root, text="Store Name", font=myfont).grid(row=4, column=0, sticky=tk.W)
        tk.Label(root, text="Progress", font=myfont).grid(row=4, column=1)
        tk.Label(root, text="Cost", font=myfont).grid(row=4, column=2, padx=10)
        tk.Label(root, text="Count", font=myfont).grid(row=4, column=3)
        tk.Label(root, text="Buy", font=myfont).grid(row=4, column=4)
        tk.Label(root, text="Unlock", font=myfont).grid(row=4, column=5)

        i = 1
        for store in Store.StoreList:
            store.display_store_info(i)
            i += 1
        print(PrintDivider)

    def display_store_info(self, i):
        self.clickbutton = tk.Button(root, text=self.StoreName, width=20, command=lambda: self.click_store())
        self.clickbutton.grid(row=4 + i, column=0, sticky=tk.W)
        self.progressbar = ttk.Progressbar(root, value=0, maximum=100, orient=tk.HORIZONTAL
                                           , length=190, mode="indeterminate")
        self.progressbar.grid(row=4+i, column=1, padx=(30, 0))
        self.store_cost_label = tk.Label(root, text=FormatMoney.format(self.StoreCost))
        self.store_cost_label.grid(row=4 + i, column=2, sticky=tk.E, padx=20)
        self.store_count_label = tk.Label(root, text=self.StoreCount)
        self.store_count_label.grid(row=4 + i, column=3, sticky=tk.E, padx=10)
        self.buybutton = tk.Button(root, text="Buy", command=lambda: self.buy_store())
        self.buybutton.grid(row=4 + i, column=4, padx=10)
        self.manager_button = tk.Button(root, text="Unlock Manager: %s" % FormatMoney.format(self.ManagerCost)
                                        , width=25, command=lambda: self.unlock_manager())
        self.manager_button.grid(row=4 + i, column=5)


    def buy_store(self):
        if self.StoreCost <= Store.Money:
            self.StoreCount += 1
            Store.Money -= self.StoreCost
            self.store_count_label.config(text=self.StoreCount)
            Game.update_ui()
        else:
            print("You don't have enough money!!!")

    def switch_button_state(self):
        if self.manager_button['state'] == tk.NORMAL:
            self.manager_button['state'] = tk.DISABLED

    def unlock_manager(self):
        if Store.Money >= self.ManagerCost and self.ManagerUnlocked is False:
            Store.Money -= self.ManagerCost
            self.ManagerUnlocked = True
            self.TimerObject.start_timer()
            Game.update_ui()
            self.switch_button_state()


    def click_store(self):
        if self.StoreCount > 0:
            self.TimerObject.start_timer()

    def make_money(self):
        dailyprofit = self.StoreProfit * self.StoreCount
        Store.Money += dailyprofit
        Game.update_ui()


class GameManager:
    def __init__(self):
        self.create_stores()
        self.display_game_header()
        Store.display_stores()

    def create_stores(self):
        # Read data from file
        with open(StoreDataFile, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                Store.StoreList.append(Store(*row))
        # Store.StoreList.append(Store("Lemonade Stand", 1.50, 3, 3, 1))
        # Store.StoreList.append(Store("Record Store", 5, 15, 10, 200))
        # Store.StoreList.append(Store("Ice Cream Store", 15, 30, 30, 5000))
        # Store.StoreList.append(Store("Guitar Store", 30, 60, 60, 10000))

    def display_game_header(self):
        root.title("Python Idle Tycoon Business Game")
        root.geometry("800x300")
        self.money_label = tk.Label(root, text=FormatMoney.format(Store.Money), font="Helvetica 15 bold")
        self.money_label.grid(row=0, column=0, sticky=tk.W)

    def update_ui(self):
        self.money_label.config(text=FormatMoney.format(Store.Money), font="Helvetica 15 bold")


# Main Game Loop



Game = GameManager()
root.mainloop()

