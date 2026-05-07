import streamlit as st
import requests

st.title("総務問い合わせ入力")
question = st.text_area("問い合わせ内容", height=160)

if st.button("APIに送信する"):
    if question.strip() == "":
        st.error("問い合わせ内容を入力してください。")
    else:
        with st.spinner("Geminiが内容を確認しています...（最大60秒）"):
            try:
                # timeout ကို 30 ကနေ 60 သို့ ပြောင်းပါ
                response = requests.post(
                    "http://127.0.0.1:8001/analyze",
                    json={"question": question},
                    timeout=60  # 30 မှ 60 သို့ပြောင်းပါ
                )
                result = response.json()
                
                st.subheader("AI解析結果")
                col1, col2 = st.columns(2)
                col1.metric("カテゴリ", result["category"])
                col2.metric("緊急度", result["priority"])
                
                st.write("**回答案:**")
                st.info(result["answer"])
            except requests.exceptions.Timeout:
                st.error("APIの応答がタイムアウトしました。もう一度お試しください。")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")