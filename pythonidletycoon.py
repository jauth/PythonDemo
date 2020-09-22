import time
import tkinter as tk
from tkinter import ttk
import csv

FormatMoney = "${:0,.2f}"
PrintDivider = "---------------------------------------------------------------"
datafile = "data.csv"

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
        self.managerCost = float(managercost)
        self.TimerObject = StoreTimer(self)

    @classmethod
    def display_stores(cls):
        store_label_col1 = tk.Label(root, text="Store Name")
        store_label_col1.grid(row=4, column=0)
        store_label_col2 = tk.Label(root, text="Progress")
        store_label_col2.grid(row=4, column=1)
        store_label_col3 = tk.Label(root, text="Store Cost")
        store_label_col3.grid(row=4, column=2)
        store_label_col3 = tk.Label(root, text="Store Count")
        store_label_col3.grid(row=4, column=3)

        i = 1
        for store in Store.StoreList:
            store.display_store_info(i)
            i += 1
        print(PrintDivider)

    def display_store_info(self, i):
        self.clickbutton = tk.Button(root, text=self.StoreName, command=lambda: self.click_store())
        self.clickbutton.grid(row=4 + i, column=0)
        self.progressbar = ttk.Progressbar(root, value=0, maximum=100, orient=tk.HORIZONTAL, length=190,
                                           mode="indeterminate")
        self.progressbar.grid(row=4+i, column=1)
        self.store_cost_label = tk.Label(root, text=FormatMoney.format(self.StoreCost))
        self.store_cost_label.grid(row=4 + i, column=2)
        self.store_count_label = tk.Label(root, text=self.StoreCount)
        self.store_count_label.grid(row=4 + i, column=3)
        self.buybutton = tk.Button(root, text="Buy", command=lambda: self.buy_store())
        self.buybutton.grid(row=4 + i, column=4)
        self.manager_button = tk.Button(root, text="Unlock Manager", command=lambda: self.unlock_manager())
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
        if Store.Money >= self.managerCost and self.ManagerUnlocked is False:
            Store.Money -= self.managerCost
            self.ManagerUnlocked = True
            self.TimerObject.start_timer()
            Game.update_ui()
            self.switch_button_state()


    def click_store(self):
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
        with open(datafile, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                Store.StoreList.append(Store(*row))
        # Store.StoreList.append(Store("Lemonade Stand", 1.50, 3, 3, 1))
        # Store.StoreList.append(Store("Record Store", 5, 15, 10, 200))
        # Store.StoreList.append(Store("Ice Cream Store", 15, 30, 30, 5000))
        # Store.StoreList.append(Store("Guitar Store", 30, 60, 60, 10000))

    def display_game_header(self):
        root.title("Python Idle Tycoon Business Game")
        root.geometry("700x300")
        money_label = tk.Label(root, text="Money")
        money_label.grid(row=0, column=0)
        self.dollars_label = tk.Label(root, text=FormatMoney.format(Store.Money))
        self.dollars_label.grid(row=1, column=0)

    def update_ui(self):
        self.dollars_label.config(text=FormatMoney.format(Store.Money))


# Main Game Loop
root = tk.Tk()

Game = GameManager()
root.mainloop()

