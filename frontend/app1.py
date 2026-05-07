import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# ページ設定（最初に設定必須）
st.set_page_config(
    page_title="総務問い合わせシステム",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSSでスタイリング
st.markdown("""
<style>
    /* メインカラーの設定 */
    :root {
        --primary-color: #1E88E5;
        --secondary-color: #FFC107;
        --success-color: #00C853;
        --error-color: #D32F2F;
    }
    
    /* ヘッダー装飾 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    /* カードデザイン */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* ステータスバッジ */
    .badge-high { background: #FF4757; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .badge-medium { background: #FFA502; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .badge-low { background: #7BEA7B; color: #333; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    
    /* サイドバーカスタマイズ */
    .css-1d391kg {
        background-color: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* ボタンデザイン */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    }
    
    /* アニメーション */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* フォーム装飾 */
    .stTextInput > div > div > input, .stSelectbox > div > div, .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'inquiries_data' not in st.session_state:
    st.session_state.inquiries_data = [
        {"id": 1, "name": "山田太郎", "question": "有給の申請方法は？", "category": "休暇", "priority": "中", "date": "2024-01-15", "status": "対応中"},
        {"id": 2, "name": "佐藤花子", "question": "健康保険証を紛失した", "category": "その他", "priority": "高", "date": "2024-01-14", "status": "完了"},
        {"id": 3, "name": "鈴木一郎", "question": "賞与の計算方法について", "category": "給与", "priority": "高", "date": "2024-01-13", "status": "未対応"},
    ]

# ヘッダー
st.markdown("""
<div class="main-header fade-in">
    <h1>🏢 総務問い合わせシステム</h1>
    <p style="font-size: 1.1rem;">お問い合わせは24時間受け付けております</p>
</div>
""", unsafe_allow_html=True)

# サイドバーメニュー
st.sidebar.markdown("## 📋 メニュー")
menu = st.sidebar.radio("", ["📝 新規問い合わせ", "📊 問い合わせ一覧", "📈 統計ダッシュボード"], label_visibility="collapsed")
st.sidebar.markdown("---")

# サイドバー情報
with st.sidebar.expander("ℹ️ お知らせ", expanded=False):
    st.info("""
    - 対応時間: 平日 9:00-18:00
    - 緊急の場合はお電話ください
    - 通常2営業日以内に回答
    """)

st.sidebar.markdown(f"""
<div class="card" style="padding: 1rem; text-align: center;">
    <small>📅 最終更新</small><br>
    <strong>{datetime.now().strftime('%Y/%m/%d %H:%M')}</strong>
</div>
""", unsafe_allow_html=True)

# メインコンテンツ
if menu == "📝 新規問い合わせ":
    st.markdown("## ✨ 新規問い合わせフォーム")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("inquiry_form", clear_on_submit=True):
            # 2カラムレイアウトで入力項目を配置
            name_col, category_col = st.columns(2)
            with name_col:
                name = st.text_input("👤 氏名 *", placeholder="例: 山田 太郎")
            with category_col:
                category = st.selectbox("📂 カテゴリ *", ["休暇", "給与", "福利厚生", "設備", "その他"])
            
            priority_col, _ = st.columns(2)
            with priority_col:
                priority = st.select_slider("🚨 緊急度", options=["低", "中", "高"], value="中")
            
            question = st.text_area("💬 問い合わせ内容 *", height=150, placeholder="詳細をご記入ください...")
            
            # ファイル添付機能を追加
            uploaded_file = st.file_uploader("📎 ファイル添付 (任意)", type=['png', 'jpg', 'pdf', 'doc', 'docx'])
            
            agree = st.checkbox("✅ 入力内容を確認しました", value=False)
            
            submitted = st.form_submit_button("🚀 送信する", use_container_width=True)
            
            if submitted:
                if not agree:
                    st.error("⚠️ 内容確認にチェックしてください")
                elif not question.strip():
                    st.error("⚠️ 問い合わせ内容を入力してください")
                elif not name.strip():
                    st.error("⚠️ 氏名を入力してください")
                else:
                    # データ保存
                    new_inquiry = {
                        "id": len(st.session_state.inquiries_data) + 1,
                        "name": name,
                        "question": question,
                        "category": category,
                        "priority": priority,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "status": "未対応"
                    }
                    st.session_state.inquiries_data.append(new_inquiry)
                    
                    # 成功メッセージ
                    st.balloons()
                    st.success("✅ 問い合わせが完了しました！担当者からの連絡をお待ちください")
                    
                    # 入力内容の確認表示（モーダル風）
                    with st.expander("📋 入力内容を確認", expanded=True):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown(f"**氏名:** {name}")
                            st.markdown(f"**カテゴリ:** {category}")
                        with col_b:
                            st.markdown(f"**緊急度:** {priority}")
                            if uploaded_file:
                                st.markdown(f"**添付ファイル:** {uploaded_file.name}")
                        st.markdown(f"**内容:**\n{question}")
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 style="margin-top: 0;">📌 お問い合わせの前に</h4>
            <ul style="padding-left: 1.2rem;">
                <li>よくある質問を確認</li>
                <li>該当するカテゴリを選択</li>
                <li>詳細に記入する</li>
            </ul>
            <hr>
            <p style="font-size: 0.9rem; color: #666;">
                💡 <strong>ヒント:</strong><br>
                具体的に記入すると、より早く解決できます。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 統計情報のミニ表示
        st.markdown("""
        <div class="card">
            <h4 style="margin-top: 0;">📊 本日の状況</h4>
        """, unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        today_str = datetime.now().strftime("%Y-%m-%d")
        with col_s1:
            today_count = len([i for i in st.session_state.inquiries_data if i['date'].startswith(today_str)])
            st.metric("受付件数", today_count, delta="+2")
        with col_s2:
            processing_count = len([i for i in st.session_state.inquiries_data if i['status'] == "対応中"])
            st.metric("対応中", processing_count, delta="")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📊 問い合わせ一覧":
    st.markdown("## 📋 問い合わせ一覧")
    
    # フィルター機能
    with st.expander("🔍 フィルター", expanded=False):
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        categories = ["全て"] + list(set([i['category'] for i in st.session_state.inquiries_data]))
        with filter_col1:
            filter_category = st.multiselect("カテゴリ", categories, default=["全て"])
        with filter_col2:
            filter_priority = st.multiselect("緊急度", ["全て", "高", "中", "低"], default=["全て"])
        with filter_col3:
            filter_status = st.multiselect("ステータス", ["全て", "未対応", "対応中", "完了"], default=["全て"])
    
    # データフィルタリング
    filtered_data = st.session_state.inquiries_data
    if filter_category and "全て" not in filter_category:
        filtered_data = [i for i in filtered_data if i['category'] in filter_category]
    if filter_priority and "全て" not in filter_priority:
        filtered_data = [i for i in filtered_data if i['priority'] in filter_priority]
    if filter_status and "全て" not in filter_status:
        filtered_data = [i for i in filtered_data if i['status'] in filter_status]
    
    # カード表示
    for idx, inquiry in enumerate(filtered_data):
        priority_class = f"badge-{inquiry['priority']}"
        priority_text = {"高": "🔴 高", "中": "🟡 中", "低": "🟢 低"}
        
        st.markdown(f"""
        <div class="card fade-in">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h3 style="margin: 0;">#{inquiry['id']} {inquiry['name']} 様</h3>
                    <p style="color: #666; margin: 5px 0;">📅 {inquiry['date']}</p>
                </div>
                <div>
                    <span class="{priority_class}">{priority_text[inquiry['priority']]}</span>
                </div>
            </div>
            <p><strong>📂 {inquiry['category']}</strong> | ステータス: {inquiry['status']}</p>
            <p><strong>内容:</strong> {inquiry['question']}</p>
            <p style="font-size: 0.9rem; color: #888;">🆔 問い合わせ番号: INQ-{inquiry['id']:04d}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # アクションボタン（デモ用）
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button(f"📝 編集", key=f"edit_{idx}"):
                st.info(f"編集機能は開発中です (ID: {inquiry['id']})")
        with col_btn2:
            if st.button(f"💬 回答", key=f"reply_{idx}"):
                st.info(f"回答機能は開発中です (ID: {inquiry['id']})")
        with col_btn3:
            if st.button(f"🗑️ 削除", key=f"delete_{idx}"):
                if st.button(f"確認", key=f"confirm_{idx}"):
                    st.session_state.inquiries_data.remove(inquiry)
                    st.rerun()
        st.markdown("---")

elif menu == "📈 統計ダッシュボード":
    st.markdown("## 📊 統計ダッシュボード")
    
    # データフレーム作成
    df = pd.DataFrame(st.session_state.inquiries_data)
    
    if not df.empty:
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            # カテゴリ別集計
            category_counts = df['category'].value_counts()
            if not category_counts.empty:
                fig1 = px.pie(values=category_counts.values, names=category_counts.index, title="カテゴリ別問い合わせ比率", color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("データがありません")
        
        with col_graph2:
            # ステータス別
            status_counts = df['status'].value_counts()
            if not status_counts.empty:
                fig2 = px.bar(x=status_counts.index, y=status_counts.values, title="ステータス別件数", color=status_counts.index, text_auto=True)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("データがありません")
        
        # 時系列推移（日付がある場合）
        if 'date' in df.columns and len(df) > 1:
            try:
                df['date_only'] = pd.to_datetime(df['date'].str.split().str[0]).dt.date
                daily_counts = df.groupby('date_only').size().reset_index(name='count')
                if len(daily_counts) > 1:
                    fig3 = px.line(daily_counts, x='date_only', y='count', title="日別問い合わせ件数推移", markers=True)
                    st.plotly_chart(fig3, use_container_width=True)
            except Exception:
                pass
        
        # KPIメトリクス
        st.markdown("### 🎯 主要KPI")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        with kpi_col1:
            st.metric("総問い合わせ数", len(df), delta="+5")
        with kpi_col2:
            high_priority = len(df[df['priority'] == "高"])
            st.metric("緊急対応必要", high_priority, delta="-2" if high_priority < 3 else "+1")
        with kpi_col3:
            completed = len(df[df['status'] == "完了"])
            st.metric("完了済み", completed, delta=f"+{completed}")
        with kpi_col4:
            response_rate = round((completed / len(df)) * 100 if len(df) > 0 else 0)
            st.metric("対応率", f"{response_rate}%", delta="+5%")

# フッター修正（エラーが発生していた部分）
st.markdown("""
<hr>
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>© 2024 総務問い合わせシステム | Powered by Streamlit</p>
    <p style="font-size: 0.8rem;">〒100-0001 東京都千代田区丸の内1-1-1 | Tel: 03-1234-5678</p>
</div>
""", unsafe_allow_html=True)