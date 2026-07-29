import json
import streamlit as st

#Transaction class létrehozása, 4 adattaggal
class Transaction:
    def __init__(self, type: str, sum: int, category: str, date: str) -> None:
        self.type = type
        self.sum = sum
        self.category = category
        self.date = date

    # Kiíratás konzolra __str__ segítségével
    def __str__(self):
        return f"[{self.type.upper()}] - {self.date} - {self.category}: {self.sum} Ft"

    #Segédmetódus a json fájlba történő mentéshez
    def to_dict(self):
        return {
            "type": self.type,
            "sum": self.sum,
            "category": self.category,
            "date": self.date
        }
'''
BudgetTracker class létrehozáse, 
a Transaction classban létrehozott példányok kezeléséhez
4 funkcióval ellátva
az __init__ részben megadjuk melyik fájlba mentjük az adatokat
létrehozunk egy üres listát amibe mentjük az objektumokat
illetve csinálunk egy betöltést,a már mentett adatokkal, hogy ne üresen induljon
'''

class BudgetTracker:
    def __init__(self, filename="budget_data.json"):
        self.filename = filename
        self.transactions = []
        self.load_data()

    #létrehoztam egy funkciót ami a transactions listába menti a kapott objektumokat, majd a json fájlba a save_to_file metódussal
    def add_transaction(self,transaction):
        self.transactions.append(transaction)
        self.save_to_file()

    #for ciklussal bevétel,kiadás kezelése
    def calculate_balance(self):
        balance = 0

        for i in self.transactions:
            if i.type == "bevétel":
                balance += i.sum
            else:
                balance -= i.sum
        return balance

    '''a Transaction classban létrehozott metódussal,
    list comprehension segítségével, az objektumokból szótárat készítünk,
    mert a JSON fájl így tudja kezelni
    plusz elmentjük az átalakított objecteket a JSON fájlba'''

    def save_to_file(self,filename="budget_data.json"):
        data_to_save = [t.to_dict() for t in self.transactions]

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        print("Sikeres mentés!")

    def load_data(self,filename="budget_data.json"):
        try:
            with open("budget_data.json", "r", encoding="utf-8") as file:
                loaded_data = json.load(file)

                self.transactions = []
                for item in loaded_data:
                    # Létrehozzuk újra a Transaction objektumokat a szótár adatai alapján
                    i = Transaction(
                        type=item["type"],
                        sum=item["sum"],
                        category=item["category"],
                        date=item["date"]
                    )
                    self.transactions.append(t)
            print("Sikeres betöltés!")


        except FileNotFoundError:
            # Ha nincs még fájl, nem történik semmi baj, indul üresen
            print("Még nincs mentett fájl, egy üres listával indulunk.")


# 1. Létrehozzuk a költségvetés-követő példányát
tracker = BudgetTracker()
'''
# 2. Létrehozunk néhány teszt tranzakciót (példányt)
t1 = Transaction("bevétel", 400000, "fizetés", "2026-06-01")
t2 = Transaction("kiadás", 15000, "élelmiszer", "2026-06-05")
t3 = Transaction("kiadás", 5000, "szórakozás", "2026-06-06")
t4 = Transaction("kiadás",6000,"élelmiszer","2026-06-08")
t5 = Transaction("kiadás",13200,"élelmiszer","2026-06-08")
t6 = Transaction("kiadás",7500,"élelmiszer","2026-06-09")
t7 = Transaction("kiadás",8900,"élelmiszer","2026-06-11")
t8 = Transaction("kiadás", 20000, "szórakozás", "2026-06-12")

# 3. Hozzáadjuk őket a trackerhez
tracker.add_transaction(t1)
tracker.add_transaction(t2)
tracker.add_transaction(t3)
tracker.add_transaction(t4)
tracker.add_transaction(t5)
tracker.add_transaction(t6)
tracker.add_transaction(t7)
tracker.add_transaction(t8)
'''



# 4. TESZT 1: Megnézzük, működik-e a __str__ (kiíratás)
print("--- AZ ÖSSZES TRANZAKCIÓ ---")
for t in tracker.transactions:
    print(t)  # Itt hívódik meg a __str__ metódusod!

# 5. TESZT 2: Kipróbáljuk a mentést JSON-be
print("\n--- MENTÉS FÁJLBA ---")
tracker.save_to_file()

# 6. TESZT 3: Kipróbáljuk a betöltést egy *új* trackerbe, hogy lássuk, visszajönnek-e az adatok
print("\n--- BETÖLTÉS ÚJ PÉLDÁNYBA ---")
new_tracker = BudgetTracker()
new_tracker.load_data()

print("Betöltött tranzakciók száma:", len(new_tracker.transactions))
for t in new_tracker.transactions:
    print(t)


loaded_tracker = BudgetTracker()

# Meghívjuk a betöltést
loaded_tracker.load_data()

print("\n--- BETÖLTÖTT TRANZAKCIÓK LISTÁJA ---")
# Végigmegyünk a betöltött elemeken és kiíratjuk őket
for t in loaded_tracker.transactions:
    print(t)

aktualis_egyenleg = tracker.calculate_balance()
print(f"\n--- AKTUÁLIS EGYENLEG ---")
print(f"Egyenleg: {aktualis_egyenleg} Ft")
