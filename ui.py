import streamlit as st
from query import search_knowledge_graph
import os


# 📌 設定 Streamlit 介面
def create_ui():
    st.title("🌐 Multi-Source Knowledge Graph Search")

    # 📖 應用說明（放在主頁最上方）
    with st.expander("📖 什麼是知識圖譜？", expanded=True):
        st.write("""
        - 這個應用可以查詢 **Wikidata、DBpedia、Google 知識圖譜**  
        - 支援 **多語言查詢**（台灣華語、英語、日語、韓語）  
        - **選擇不同 API 來源** 並輸入關鍵字，即可查詢
        """)

    # 📡 選擇知識圖譜 API
    API_OPTIONS = ["Wikidata", "DBpedia", "Google Knowledge Graph"]
    selected_api = st.radio("📡 選擇知識圖譜 API", API_OPTIONS, index=0)

    # 🌍 選擇語言（僅 Wikidata 適用）
    LANGUAGE_MAPPING = {
        "English": "en",
        "台灣華語": "zh-tw",
        "日本語": "ja",
        "한국어": "ko"
    }
    selected_lang = st.selectbox("🌍 選擇語言（僅 Wikidata 適用）", list(LANGUAGE_MAPPING.keys()))
    lang_code = LANGUAGE_MAPPING[selected_lang]

    # 🔑 Google API Key（如果選擇 Google Knowledge Graph）
    google_api_key = None
    if selected_api == "Google Knowledge Graph":
        with st.expander("🔑 設定 Google Knowledge Graph API Key"):
            google_api_key = st.text_input("請輸入 API Key", type="password")
            if not google_api_key:
                google_api_key = os.getenv("GOOGLE_KG_API_KEY")  # 使用環境變數或 Secrets

    # 🔍 輸入查詢關鍵字
    keyword = st.text_input("🔍 輸入關鍵字（例如：Elon Musk, 台積電）", help="請輸入人物、公司或地點名稱")

    # 📌 按鈕（使用 st.session_state 儲存狀態）
    if st.button("🚀 查詢", key="search_button"):
        with st.spinner("查詢中，請稍候..."):
            name, description, image_url = search_knowledge_graph(keyword, selected_api, lang_code, google_api_key)

            if name:
                st.subheader(f"🔹 {name}")
                st.markdown(f"📖 **描述**: {description}")

                if selected_api == "Wikidata":
                    st.info("🌍 來自 Wikidata，數據較完整")

                if selected_api == "DBpedia":
                    st.info("📖 來自 DBpedia，結構化維基百科")

                if selected_api == "Google Knowledge Graph":
                    st.info("🔍 來自 Google 知識圖譜，適合熱門人物查詢")

                if image_url is not None:
                    st.image(image_url, caption=name)
            else:
                st.warning(description)

    # 📌 側邊欄（放開發資訊 & 注意事項）
    with st.sidebar:
        st.header("👨‍💻 開發者資訊")
        st.markdown("""
        - **開發者**: 余彦志 （大宇 / ian）
        - **技術棧**: Streamlit, Python, Wikidata API, DBpedia, Google KG
        - **聯絡方式**: [dayuian@hotmail.com](mailto:dayuian@hotmail.com)
        """)

        with st.expander("⚠️ 注意事項", expanded=False):
            st.write("""
            - **Wikidata** 可能無法查詢所有內容，請切換 API 測試  
            - **Google 知識圖譜 API** 需要 API Key，請前往 [Google Cloud Console](https://console.cloud.google.com/) 申請  
            - **部分查詢結果可能不完整**，請嘗試 **不同名稱或語言**  
            """)

        with st.expander("📌 資料來源", expanded=False):
            st.write("""
            - [Wikidata API](https://www.wikidata.org/wiki/Wikidata:Data_access)  
            - [DBpedia API](https://wiki.dbpedia.org/)  
            - [Google Knowledge Graph API](https://developers.google.com/knowledge-graph/)  
            """)
