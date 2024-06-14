import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="物理用語ガチャ")

# タイトルと説明
st.title('物理用語ガチャ')

st.write('物理用語をランダムに表示して、勉強をサポートします！')
st.write('がんばってください！')

# Load the data
@st.cache
def load_data():
    return pd.read_excel("物理公式集.xlsx")

words_df = load_data()

# ガチャ機能
if st.button('ガチャを引く！'):
    rarity_probs = {
        'N': 0.4,
        'R': 0.3,
        'SR': 0.2,
        'SSR': 0.1
    }
    chosen_rarity = np.random.choice(list(rarity_probs.keys()), p=list(rarity_probs.values()))
    subset_df = words_df[words_df['難易度'] == chosen_rarity]
    selected_word = subset_df.sample().iloc[0]
    
    # セッションステートに選択された単語を保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False

if 'selected_word' in st.session_state:
    st.header(f"用語名: {st.session_state.selected_word['用語']}")
    st.subheader(f"難易度: {st.session_state.selected_word['難易度']}")

    # 意味を確認するボタンを追加
    if st.button('意味を確認する'):
        st.session_state.display_meaning = True

    if st.session_state.display_meaning:
        st.write(f"用語の意味: {st.session_state.selected_word['用語の意味']}")