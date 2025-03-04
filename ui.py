import streamlit as st
from query import search_wikidata

# 📌 設定 Streamlit 介面
def create_ui():
    st.title("🌐 Wikidata 知識圖譜查詢")

    # 📌 應用說明（放在主頁最上方）
    st.markdown("""
    ## 📖 應用說明
    - 本應用透過 **Wikidata API** 查詢知識圖譜  
    - 您可以輸入 **人名、公司、地點** 來獲取詳細資訊  
    - **支援多語言查詢**（台灣華語、英語、日語、韓語）  
    """)

    # 📌 選擇語言
    LANGUAGE_MAPPING = {
        "English": "en",
        "台灣華語": "zh-tw",
        "日本語": "ja",
        "한국어": "ko"
    }
    selected_lang = st.selectbox("🌍 選擇語言", list(LANGUAGE_MAPPING.keys()))
    lang_code = LANGUAGE_MAPPING[selected_lang]

    # 📌 輸入框
    keyword = st.text_input("🔍 輸入關鍵字（例如：Trump, 蔡英文）")

    # 📌 按鈕
    if st.button("查詢"):
        name, description, image_url = search_wikidata(keyword, lang_code)

        if name:
            st.markdown(f"**🔹 名稱**: {name}")
            st.markdown(f"**📖 描述**: {description}")
            
            if image_url:
                st.image(image_url, caption=name)
        else:
            st.warning(description)

    # 📌 側邊欄（放開發資訊 & 注意事項）
    with st.sidebar:
        st.header("👨‍💻 開發者資訊")
        st.markdown("""
        - **開發者**: 余彦志 （大宇 / ian）
        - **技術棧**: Streamlit, Python, Wikidata API
        - **聯絡方式**: [dayuian@hotmail.com](mailto:dayuian@hotmail.com)
        """)

        st.header("⚠️ 注意事項")
        st.markdown("""
        - 部分查詢結果可能不完整，因為 **Wikidata** 可能沒有該資訊  
        - 若查詢失敗，請嘗試 **不同的名稱或語言**  
        """)

        st.header("📌 資料來源")
        st.markdown("""
        - [Wikidata API](https://www.wikidata.org/wiki/Wikidata:Data_access)  
        """)

