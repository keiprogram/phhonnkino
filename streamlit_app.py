import streamlit as st
import pandas as pd
import numpy as np
import threading
import time

st.set_page_config(page_title="物理用語ガチャ")

# CSSを使用してタイトルを中央揃えにするスタイルを適用し、背景色を変更する
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        color:#0D5661;
    }
    .centered-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .stApp {
        background-color: #FCFAF2;
    }
    .start-screen {
        background-image: url('https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDJ1MmoyejJ3bzQwNTJ0bDdmaGJhNTNwNHJlNjg4aTF6M3MyMWhxOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5xtDarwBWrq3CBqqs5G/giphy.gif');
        background-size: cover;
        background-position: center;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .counter-box {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
    }
    .counter {
        font-size: 24px;
        font-weight: bold;
        color: #0D5661;
        background-color: #f2f2f2;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
    }
    .timer {
        font-size: 24px;
        font-weight: bold;
        color: #FF0000;
        text-align: center;
    }
    .big-button {
        font-size: 24px;
        padding: 20px 40px;
        border-radius: 10px;
        background-color: #0D5661;
        color: #FFFFFF;
        border: none;
        cursor: pointer;
    }
    .big-button:hover {
        background-color: #094A5A;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 初期状態の設定
if 'started' not in st.session_state:
    st.session_state.started = False
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'incorrect_count' not in st.session_state:
    st.session_state.incorrect_count = 0
if 'timer_expired' not in st.session_state:
    st.session_state.timer_expired = False
if 'time_left' not in st.session_state:
    st.session_state.time_left = 10
if 'progress_bar' not in st.session_state:
    st.session_state.progress_bar = 100

def start_timer():
    st.session_state.timer_expired = False
    st.session_state.time_left = 10
    st.session_state.progress_bar = 100
    timer_thread = threading.Thread(target=run_timer)
    timer_thread.start()

def run_timer():
    while st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.session_state.progress_bar -= 10
        st.experimental_rerun()
    set_timer_expired()

def set_timer_expired():
    st.session_state.timer_expired = True
    st.session_state.quiz_answered = True
    st.session_state.selected_choice = None  # タイムアウト時は選択なしとする
    st.experimental_rerun()

# スタート待機画面
if not st.session_state.started:
    st.markdown('<div class="start-screen">', unsafe_allow_html=True)
    st.markdown('<h2 class="centered-title">スタートボタンを押して始めてください</h2>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="centered-button">', unsafe_allow_html=True)
        if st.button('スタート', key='start', use_container_width=True, help='クリックして開始'):
            st.session_state.started = True
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ゲーム画面
if st.session_state.started:
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
    with st.container():
        st.markdown('<div class="centered-button">', unsafe_allow_html=True)
        if st.button('ガチャを引く！', key='gacha', use_container_width=True):
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
            other_words = words_df[words_df['用語'] != selected_word['用語']].sample(4)
            choices = other_words['用語の意味'].tolist() + [selected_word['用語の意味']]
            np.random.shuffle(choices)
            
            # セッションステートに選択された単語とクイズ選択肢を保存
            st.session_state.selected_word = selected_word
            st.session_state.choices = choices
            st.session_state.correct_answer = selected_word['用語の意味']
            st.session_state.display_meaning = False
            st.session_state.quiz_answered = False

            # タイマーをスタート
            start_timer()
        st.markdown('</div>', unsafe_allow_html=True)

    if 'selected_word' in st.session_state:
        st.header(f"用語名: {st.session_state.selected_word['用語']}")
        st.subheader(f"難易度: {st.session_state.selected_word['難易度']}")

        # クイズを表示
        st.write("この用語の意味はどれでしょう？")
        quiz_answer = st.radio("選択肢", st.session_state.choices)
        
        with st.container():
            st.markdown('<div class="centered-button">', unsafe_allow_html=True)
            if st.button('回答する', key='answer', use_container_width=True):
                st.session_state.quiz_answered = True
                st.session_state.selected_choice = quiz_answer
            st.markdown('</div>', unsafe_allow_html=True)

        # プログレスバーでタイマーを視覚化
        st.progress(st.session_state.progress_bar)
        st.markdown(f'<div class="timer">残り時間: {st.session_state.time_left}秒</div>', unsafe_allow_html=True)

        if st.session_state.quiz_answered:
            if st.session_state.selected_choice == st.session_state.correct_answer:
                st.success("正解です！", icon="✅")
                st.session_state.correct_count += 1
            else:
                st.error("不正解です。", icon="❌")
                st.session_state.incorrect_count += 1
            st.write(f"正しい意味: {st.session_state.correct_answer}")

    # 正解と不正解の回数を表示
    st.markdown(
        f"""
        <div class="counter-box">
            <div class="counter">正解: {st.session_state.correct_count}</div>
            <div class="counter">不正解: {st.session_state.incorrect_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
