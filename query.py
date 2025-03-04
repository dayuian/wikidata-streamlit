import requests

# 📌 Wikidata 查詢 API
def query_wikidata(entity_id, lang="en"):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        entity_data = data["entities"].get(entity_id, {})

        # 取得名稱 & 描述
        name = entity_data["labels"].get(lang, {}).get("value", "無資料")
        description = entity_data["descriptions"].get(lang, {}).get("value", "無描述")

        # 取得圖片（如果有）
        image_url = None
        if "P18" in entity_data["claims"]:
            image_info = entity_data["claims"]["P18"][0]["mainsnak"]["datavalue"]["value"]
            image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{image_info}"

        return name, description, image_url
    else:
        return None, "❌ 查詢失敗，請確認輸入的關鍵字是否正確！", None

# 📌 查詢 Wikidata ID
def search_wikidata(keyword, lang="en"):
    search_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={keyword}&language={lang}&format=json"
    response = requests.get(search_url)

    if response.status_code == 200:
        search_results = response.json()
        if search_results["search"]:
            entity_id = search_results["search"][0]["id"]
            return query_wikidata(entity_id, lang)
        else:
            return None, "❌ 找不到相關資訊，請嘗試其他關鍵字！", None
    else:
        return None, "❌ 查詢失敗，請稍後再試！", None
