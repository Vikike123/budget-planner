import streamlit as st
from main import BudgetTracker, Transaction

if 'tracker' not in st.session_state:
    st.session_state.tracker = BudgetTracker()

# Előre definiált kategóriák listája (ezt bármikor bővítheted)
KIADAS_KATEGORIAK = ["élelmiszer", "szórakozás", "lakhatás", "közlekedés", "egyéb"]
BEVETEL_KATEGORIAK = ["fizetés", "ajándék", "mellékállás", "egyéb"]

st.title("💰 Személyes Költségvetés-tervező")
fooldal_ful, admin_ful = st.tabs(["🏠 Főoldal (Adatbevitel)", "⚙️ Admin / Szűrések"])

with fooldal_ful:
    st.subheader("Új tranzakció rögzítése")

    # Kategória listák
    KIADAS_KATEGORIAK = ["élelmiszer", "szórakozás", "lakhatás", "közlekedés", "egyéb"]
    BEVETEL_KATEGORIAK = ["fizetés", "ajándék", "mellékállás", "egyéb"]

    t_type = st.selectbox("Típus", ["kiadás", "bevétel"], key="main_type")

    if t_type == "kiadás":
        category = st.selectbox("Kategória", KIADAS_KATEGORIAK, key="main_cat_kiadas")
    else:
        category = st.selectbox("Kategória", BEVETEL_KATEGORIAK, key="main_cat_bevetel")

    with st.form("transaction_form"):
        amount = st.number_input("Összeg (Ft)", min_value=1, step=100)
        date = st.date_input("Dátum")
        submit_button = st.form_submit_button(label="Hozzáadás és Mentés")

        if submit_button:
            new_t = Transaction(t_type, amount, category, str(date))
            st.session_state.tracker.add_transaction(new_t)
            st.success(f"✅ Sikeresen rögzítve: {category} ({amount} Ft)")
            st.rerun()

    st.divider()
    # Gyors egyenleg mutató a főoldalon
    balance = st.session_state.tracker.calculate_balance()
    st.metric(label="Aktuális egyenleg", value=f"{balance} Ft")

# --- 2. FÜL: ADMIN FELÜLET (Szűrés, Rendezés, Részletek) ---
with admin_ful:
    st.subheader("⚙️ Tranzakciók kezelése és törlése")

    # Ha nincsenek tranzakciók, szólnunk kell
    if len(st.session_state.tracker.transactions) == 0:
        st.info("Nincsenek rögzített tranzakciók a rendszerben.")
    else:
        # --- TÖRLÉSI SZEKCIÓ ---
        st.markdown("### 🗑️ Tranzakció törlése")

        # Létrehozunk egy listát a legördülőhöz, amiben látszanak az adatok, hogy tudjuk, mit törlünk
        # A listaelem mellett feltüntetjük az indexét is, hogy pontosan tudjuk, mit kell törölni
        tranzakcio_opciok = []
        for index, t in enumerate(st.session_state.tracker.transactions):
            szoveg = f"[{index}] {t.date} - {t.type.upper()} - {t.category}: {t.sum} Ft"
            tranzakcio_opciok.append((index, szoveg))

        # Kifejtjük a kiválasztáshoz (csak a szövegeket mutatjuk a felhasználónak)
        kivalasztott_szoveg = st.selectbox(
            "Válaszd ki a törölni kívánt tételt:",
            options=[item[1] for item in tranzakcio_opciok]
        )

        if st.button("Kiválasztott tétel törlése", type="primary"):
            # Megkeressük a kiválasztott szöveghez tartozó indexet
            torlendo_index = None
            for item in tranzakcio_opciok:
                if item[1] == kivalasztott_szoveg:
                    torlendo_index = item[0]
                    break

            if torlendo_index is not None:
                # 1. Kiveszük az elemet a memóriából a sorszáma alapján
                torlendo_elem = st.session_state.tracker.transactions.pop(torlendo_index)

                # 2. Elmentjük a frissített listát a JSON fájlba
                st.session_state.tracker.save_to_file()

                st.success(f"Sikeresen törölve: {torlendo_elem.category} ({torlendo_elem.sum} Ft)")

                # Kicsit várunk, majd frissítjük az oldalt
                import time

                time.sleep(1)
                st.rerun()


        # --- ÖSSZES TÖRLÉSE SZEKCIÓ ---
        st.divider()
        st.markdown("### ⚠️ Veszélyes zóna")

        # Biztonsági jelölőnégyzet, hogy ne lehessen véletlenül törölni
        biztos_az_osszes = st.checkbox("Biztosan törölni szeretnéd az ÖSSZES tranzakciót?")

        if st.button("🗑️ ÖSSZES tranzakció törlése", type="secondary"):
            if biztos_az_osszes:
                # 1. Kiürítjük a listát a memóriában
                st.session_state.tracker.transactions = []

                # 2. Elmentjük a boszorkánykonyhában az üres listát a JSON fájlba
                st.session_state.tracker.save_to_file()

                st.success("Minden tranzakció sikeresen törölve!")

                import time

                time.sleep(1)
                st.rerun()
            else:
                st.warning("Kérlek, pipáld be a megerősítő dobozt a törléshez!")

        st.divider()

    # Szűrési és rendezési elemek az admin fülön
    szurt_tipus = st.selectbox("Szűrés típus szerint", ["Összes", "bevétel", "kiadás"], key="admin_filter")

    rendezes = st.selectbox("Rendezés", [
        "Alapértelmezett (rögzítési sorrend)",
        "Összeg: Növekvő",
        "Összeg: Csökkenő",
        "Kategória (ABC)"
    ], key="admin_sort")

    # Adatok másolása a szűréshez
    megjelenitendo_tranzakciok = st.session_state.tracker.transactions.copy()

    # Szűrés logika
    if szurt_tipus != "Összes":
        megjelenitendo_tranzakciok = [t for t in megjelenitendo_tranzakciok if t.type == szurt_tipus]

    # Rendezés logika
    if rendezes == "Összeg: Növekvő":
        megjelenitendo_tranzakciok.sort(key=lambda t: t.sum)
    elif rendezes == "Összeg: Csökkenő":
        megjelenitendo_tranzakciok.sort(key=lambda t: t.sum, reverse=True)
    elif rendezes == "Kategória (ABC)":
        megjelenitendo_tranzakciok.sort(key=lambda t: t.category)

    st.divider()

    # Eredmények kiíratása az admin fülön
    if len(megjelenitendo_tranzakciok) == 0:
        st.info("Nincs a szűrésnek megfelelő tranzakció.")
    else:
        st.write(f"Találatok száma: **{len(megjelenitendo_tranzakciok)} db**")
        for t in megjelenitendo_tranzakciok:
            st.write(f"- **{t.date}** | **{t.type.upper()}** | {t.category}: **{t.sum} Ft**")