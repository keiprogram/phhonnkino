import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="物理用語ガチャ")

# タイトルと説明
st.title('物理用語ガチャ')
st.write('物理の用語をランダムに表示して、勉強をサポートします！')
st.write('がんばってください！')

# データの読み込み関数
@st.cache_data
def load_data():
    file_path = '/mnt/data/物理公式集.xlsx'  # アップロードされたファイルのパス
    return pd.read_excel(file_path)

# データを読み込む
words_df = load_data()

# ガチャ機能
if st.button('ガチャを引く！'):
    rarity_probs = {
        '一般用語': 0.4,
        '専門用語': 0.3,
        '専門用語（難）': 0.2,
        '専門用語（超難）': 0.1
    }
    chosen_rarity = np.random.choice(list(rarity_probs.keys()), p=list(rarity_probs.values()))
    subset_df = words_df[words_df['レア度'] == chosen_rarity]
    selected_word = subset_df.sample().iloc[0]
    
    # セッションステートに選択された単語を保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False

# 選択された単語を表示
if 'selected_word' in st.session_state:
    st.header(f"用語名: {st.session_state.selected_word['用語']}")
    st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")

    # 意味を確認するボタンを追加
    if st.button('意味を確認する'):
        st.session_state.display_meaning = True

    if st.session_state.display_meaning:
        st.write(f"意味: {st.session_state.selected_word['意味']}")
