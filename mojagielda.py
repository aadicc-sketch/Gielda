import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Giełda PRO", page_icon="📊", layout="wide")

st.title("Monitor Świecowy: IRON & OUST 🕯️")

# 1. Boczne menu (opcjonalnie, żeby było czyściej)
with st.sidebar:
    wybor = st.selectbox("Wybierz spółkę:", ["IRON", "OUST", "AAPL", "TSLA", "CDR.WA"])
    
    interwaly = {
        "5 Minut": "5m",
        "15 Minut": "15m",
        "1 Godzina": "1h",
        "Dzień": "1d"
    }
    wybrany_opis = st.radio("Interwał:", list(interwaly.keys()))
    kod_interwalu = interwaly[wybrany_opis]

# Ustawienie zakresu danych
zakres = "5d" if kod_interwalu in ["5m", "15m"] else "1mo"

# 2. Pobieranie danych
data = yf.Ticker(wybor)
historia = data.history(period=zakres, interval=kod_interwalu)

if not historia.empty:
    # 3. Tworzenie wykresu świecowego
    fig = go.Figure(data=[go.Candlestick(
        x=historia.index,
        open=historia['Open'],
        high=historia['High'],
        low=historia['Low'],
        close=historia['Close'],
        name='Kurs'
    )])

    # Wygląd wykresu
    fig.update_layout(
        title=f"Wykres świecowy {wybor}",
        yaxis_title="Cena (USD)",
        xaxis_rangeslider_visible=False, # Usuwamy suwak na dole dla czytelności
        template="plotly_dark" # Ciemny motyw wygląda bardzo pro!
    )

    # Wyświetlenie wykresu w Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # 4. Statystyki pod wykresem
    col1, col2, col3 = st.columns(3)
    col1.metric("Max", f"{round(historia['High'].max(), 2)}$")
    col2.metric("Min", f"{round(historia['Low'].min(), 2)}$")
    col3.metric("Zamknięcie", f"{round(historia['Close'].iloc[-1], 2)}$")

else:
    st.error("Brak danych dla tego interwału.")
