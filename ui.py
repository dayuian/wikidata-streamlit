import streamlit as st
from query import search_wikidata

# 📌 設定 Streamlit 介面
def create_ui():
    st.title("🌐 Wikidata 知識圖譜查詢")
    st.write("🔎 輸入一個**人名、公司、地點**，系統將查詢 Wikidata 知識圖譜並顯示相關資訊。")

    # 選擇語言
    lang = st.selectbox("🌍 選擇語言", ["en", "zh"])

    # 輸入框
    keyword = st.text_input("🔍 輸入關鍵字（例如：Elon Musk, Tesla）")

    # 按鈕
    if st.button("查詢"):
        name, description, image_url = search_wikidata(keyword, lang)

        if name:
            st.markdown(f"**🔹 名稱**: {name}")
            st.markdown(f"**📖 描述**: {description}")
            
            if image_url:
                st.image(image_url, caption=name)
        else:
            st.warning(description)
