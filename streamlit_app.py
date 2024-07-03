import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="物理用語ガチャ")

# GIFのURLを指定
background_gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnA1bnhwMHQ1M2xjYnAyYXJlNnFqOWZub3Z4aXZ0dHJkbndnM204bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5xtDarwBWrq3CBqqs5G/giphy.gif"

# CSSを使用して背景をGIFに設定し、白色のぼかしを追加
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("{background_gif_url}") no-repeat center center fixed;
        background-size: cover;
        filter: blur(5px) brightness(0.7);
    }}
    </style>
    """,
    unsafe_allow_html=True
)



# CSSを使用してタイトルを中央揃えにするスタイルを適用する
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        color:#0D5661;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="物理用語ガチャ")

# GIFのURLを指定
background_gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnA1bnhwMHQ1M2xjYnAyYXJlNnFqOWZub3Z4aXZ0dHJkbndnM204bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5xtDarwBWrq3CBqqs5G/giphy.gif"

# CSSを使用して背景をGIFに設定し、白色のぼかしを追加
st.markdown(
    f"""
    <style>
    .stApp {{
        background: white;
        position: relative;
        z-index: 1;
    }}
    .stApp::before {{
        content: "";
        background: url("{background_gif_url}") no-repeat center center fixed;
        background-size: cover;
        filter: blur(10px) brightness(0.7);
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: -1;
    }}
    </style>
    """,
    unsafe_allow_html=True
)



# CSSを使用してタイトルを中央揃えにするスタイルを適用する
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        color:#0D5661;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 中央揃えスタイルを適用したタイトル
st.markdown('<h1 class="centered-title">高校物理用語ガチャ</h1>', unsafe_allow_html=True)

# その他の説明
st.write('物理用語をランダムに表示して、勉強をサポートします！')
st.write('範囲は高校で習う物理用語です')
st.write('がんばってください！')

# Load the data
@st.cache_data
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
    st.header(f"用語名: {st.session_state.selected_word['用語']}")
    st.subheader(f"難易度: {st.session_state.selected_word['難易度']}")

    # クイズを表示
    st.write("この用語の意味はどれでしょう？")
    quiz_answer = st.radio("選択肢", st.session_state.choices)
    
    if st.button('回答する'):
        st.session_state.quiz_answered = True
        st.session_state.selected_choice = quiz_answer

    if st.session_state.quiz_answered:
        if st.session_state.selected_choice == st.session_state.correct_answer:
            st.success("正解です！", icon="✅")
        else:
            st.error("不正解です。", icon="❌")
        st.write(f"正しい意味: {st.session_state.correct_answer}")
