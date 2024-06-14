import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="物理用語ガチャ")

# タイトルと説明
st.markdown("<h1 style='text-align: center;'>高校物理用語ガチャ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>物理用語をランダムに表示して、勉強をサポートします！</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>範囲は高校で習う物理用語です</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>がんばってください！</p>", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    return pd.read_excel("物理公式集.xlsx")

words_df = load_data()

# ガチャ機能
center_button = st.columns([3, 1, 3])[1]
with center_button:
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

        # クイズ用の選択肢を生成
        other_words = words_df[words_df['用語'] != selected_word['用語']].sample(2)
        choices = other_words['用語の意味'].tolist() + [selected_word['用語の意味']]
        np.random.shuffle(choices)

        # セッションステートに選択された単語とクイズ選択肢を保存
        st.session_state.selected_word = selected_word
        st.session_state.choices = choices
        st.session_state.correct_answer = selected_word['用語の意味']
        st.session_state.display_meaning = False
        st.session_state.quiz_answered = False

if 'selected_word' in st.session_state:
    st.markdown(f"<h2 style='text-align: center;'>用語名: {st.session_state.selected_word['用語']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>難易度: {st.session_state.selected_word['難易度']}</h3>", unsafe_allow_html=True)

    # クイズを表示
    st.markdown("<p style='text-align: center;'>この用語の意味はどれでしょう？</p>", unsafe_allow_html=True)
    quiz_answer = st.radio("選択肢", st.session_state.choices, index=0, horizontal=True)
    
    center_submit = st.columns([3, 1, 3])[1]
    with center_submit:
        if st.button('回答する'):
            st.session_state.quiz_answered = True
            st.session_state.selected_choice = quiz_answer

    if st.session_state.quiz_answered:
        if st.session_state.selected_choice == st.session_state.correct_answer:
            st.success("正解です！", icon="✅")
        else:
            st.error("不正解です。", icon="❌")
        st.write(f"正しい意味: {st.session_state.correct_answer}")

    center_meaning = st.columns([3, 1, 3])[1]
    with center_meaning:
        # 意味を確認するボタンを追加
        if st.button('意味を確認する'):
            st.session_state.display_meaning = True

    if st.session_state.display_meaning:
        st.markdown(f"<p style='text-align: center;'>用語の意味: {st.session_state.selected_word['用語の意味']}</p>", unsafe_allow_html=True)
