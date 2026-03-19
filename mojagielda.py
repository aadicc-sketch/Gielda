import streamlit as st
import yfinance as yf

# Ustawienia strony - fajna ikona dolara w karcie przeglądarki
st.set_page_config(page_title="Mój Giełdowy Radar", page_icon="💰")

st.title("Monitor Akcji: IREN & OUST 📈")

# Tworzymy listę spółek do wyboru
spolki = ["IREN", "OUST"]
wybor = st.selectbox("Wybierz spółkę, którą chcesz sprawdzić:", spolki)

# Pobieranie danych dla wybranej spółki
data = yf.Ticker(wybor)

# Pobieramy historię z ostatniego miesiąca
historia = data.history(period="1mo")

if not historia.empty:
    # Pobieramy ostatnią dostępną cenę
    aktualna_cena = historia['Close'].iloc[-1]
    wczorajsza_cena = historia['Close'].iloc[-2]
    roznica = aktualna_cena - wczorajsza_cena

    # Wyświetlamy duże cyfry z ceną i zmianą (zielone/czerwone)
    st.metric(label=f"Cena {wybor}", value=f"{round(aktualna_cena, 2)} USD", delta=f"{round(roznica, 2)} USD")

    # Rysujemy wykres
    st.subheader(f"Wykres kursu {wybor} (ostatni miesiąc)")
    st.line_chart(historia['Close'])
    
   # Dodajemy sekcję z newsami (BEZPIECZNIEJSZA WERSJA)
    st.subheader(f"Najnowsze wieści o {wybor}")
    newsy = data.news[:3] # Pobierz 3 najnowsze wiadomości
    
    if not newsy:
        st.write("Brak aktualnych newsów dla tej spółki.")
    else:
        for n in newsy:
            # Używamy .get(), który nie wywala błędu, jeśli czegoś brakuje
            tytul = n.get('title', 'Brak tytułu')
            link = n.get('link', '#')
            zrodlo = n.get('publisher', 'Nieznane źródło')
            
            st.write(f"**[{tytul}]({link})**")
            st.write(f"Źródło: {zrodlo}")
            st.divider()
        st.divider()
else:
    st.error("Nie udało się pobrać danych. Sprawdź połączenie z internetem.")
