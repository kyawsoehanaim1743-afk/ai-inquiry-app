import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="総務問い合わせ入力", page_icon="📝")


st.sidebar.title("メニュー")
page = st.sidebar.radio("ページ", ["問い合わせ入力", "履歴一覧"])


if page == "問い合わせ入力":
    st.title("総務問い合わせ入力")
    st.write("社員から総務への問い合わせを入力してください。")
    
    with st.form("inquiry_form"):
        name = st.text_input("氏名")
        category = st.selectbox("カテゴリ", ["休暇", "給与", "福利厚生", "その他"])
        priority = st.radio("緊急度", ["高", "中", "低"])
        question = st.text_area("問い合わせ内容", height=160)
        agree = st.checkbox("内容を確認しました")
        
        submitted = st.form_submit_button("送信する")
    
    if submitted:
        if not agree:
            st.error("内容確認にチェックしてください")
        elif question.strip() == "":
            st.error("問い合わせ内容を入力してください")
        else:
            with st.spinner("処理中..."):
                try:
                    # API ကို category နဲ့ priority ပါ ပို့မယ်
                    response = requests.post(
                        f"{API_URL}/analyze",
                        json={
                            "question": question,
                            "category": category,
                            "priority": priority,
                            "name": name
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ 登録が完了しました")
                        
                        # ရလဒ်ပြမယ်
                        st.subheader("登録内容")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("カテゴリ", result["category"])
                        with col2:
                            st.metric("緊急度", result["priority"])
                        
                        st.write("**回答:**")
                        st.info(result["answer"])
                        
                        st.subheader("入力内容")
                        st.write("氏名:", name if name else "未入力")
                        st.write("カテゴリ:", category)
                        st.write("緊急度:", priority)
                        st.write("内容:", question)
                    else:
                        st.error(f"エラー: {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Backendサーバーに接続できません (port 8000 を確認)")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")


else:  
    st.title("問い合わせ一覧")

    try:
        response = requests.get(f"{API_URL}/inquiries", timeout=10)
        if response.status_code == 200:
            inquiries = response.json()
            if inquiries:
                for idx, item in enumerate(inquiries):
                    unique_key = f"delete_{item['id']}_{idx}"

                    with st.expander(f"[{item['id']}] {item['created_at']} - {item['question'][:50]}..."):
                        st.write(f"**カテゴリ:** {item['category']}")
                        st.write(f"**緊急度:** {item['priority']}")
                        st.write(f"**回答:** {item['answer']}")
                        st.write(f"**質問全文:** {item['question']}")

                        #DELETE BUTTON 
                        col1, col2, col3 = st.columns([1, 1, 4])
                        with col1:
                            if st.button(f"🗑️ 削除", key=unique_key):
                                try:
                                    delete_response = requests.delete(f"{API_URL}/inquiries/{item['id']}")
                                    if delete_response.status_code == 200:
                                        st.success(f"ID {item['id']} を削除しました")
                                        st.rerun()  
                                    else:
                                        st.error("削除に失敗しました")
                                except Exception as e:
                                    st.error(f"エラー: {e}")
                        
            else:
                st.info("まだ問い合わせはありません。")
        else:
            st.warning("APIからデータを取得できませんでした。")
    except requests.exceptions.ConnectionError:
        st.warning("Backendサーバーに接続できません。バックエンドを起動してください。")
    except Exception as e:
        st.error(f"一覧取得エラー: {e}")


st.divider()
st.info("担当者が回答するまでお待ちください")