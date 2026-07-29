from main import Transaction, BudgetTracker


def test_add_transaction_and_balance():
    # Előkészület
    # A tesztben:
    tracker = BudgetTracker(filename="test_budget_data.json")
    tracker.transactions = []  # Ürítjük a teszthez

    t1 = Transaction("bevétel", 100000, "fizetés", "2026-07-01")
    t2 = Transaction("kiadás", 20000, "étel", "2026-07-02")

    # Művelet
    tracker.add_transaction(t1)
    tracker.add_transaction(t2)

    # Ellenőrzés (itt egyszerűen az assert kulcsszót használjuk!)
    assert tracker.calculate_balance() == 80000
    assert len(tracker.transactions) == 2


def test_transaction_string_format():
    t = Transaction("kiadás", 5000, "kávé", "2026-07-29")

    # Ellenőrizzük a __str__ kimenetét
    assert str(t) == "[KIADÁS] - 2026-07-29 - kávé: 5000 Ft"