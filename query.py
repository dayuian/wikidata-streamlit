import requests

# 📌 先查詢 Wikidata QID（必要步驟）
def get_wikidata_qid(keyword):
    try:
        search_url = f"https://www.wikidata.org/w/api.php?action=query&list=search&srsearch={keyword}&format=json"
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if "query" in data and "search" in data["query"] and len(data["query"]["search"]) > 0:
            qid = data["query"]["search"][0]["title"]  # 取得第一個 QID
            return qid
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

# 📌 用 QID 查詢 Wikidata 詳細資訊
def query_wikidata(keyword, lang="en"):
    try:
        qid = get_wikidata_qid(keyword)
        if not qid:
            return None, "⚠️ Wikidata 找不到此條目，請嘗試不同的關鍵字！", None

        url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        entity_data = data["entities"].get(qid, {})

        if not entity_data:
            return None, "⚠️ Wikidata 無法找到詳細資訊！", None

        name = entity_data["labels"].get(lang, {}).get("value", keyword)
        description = entity_data["descriptions"].get(lang, {}).get("value", "無描述")

        # 取得圖片
        image_url = None
        if "P18" in entity_data["claims"]:
            image_info = entity_data["claims"]["P18"][0]["mainsnak"]["datavalue"]["value"]
            image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{image_info}"

        return name, description, image_url

    except requests.exceptions.Timeout:
        return None, "❌ API 連線超時，請稍後再試！", None
    except requests.exceptions.RequestException as e:
        return None, f"❌ API 請求錯誤: {str(e)}", None

# 📌 DBpedia 查詢 API
def query_dbpedia(keyword):
    try:
        url = f"https://dbpedia.org/data/{keyword.replace(' ', '_')}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        entity_uri = f"http://dbpedia.org/resource/{keyword.replace(' ', '_')}"
        entity_data = data.get(entity_uri, {})

        if not entity_data:
            return None, "⚠️ DBpedia 無此條目，請更換關鍵字！", None

        name = keyword
        description = entity_data.get("http://www.w3.org/2000/01/rdf-schema#comment", [{}])[0].get("value", "無描述")
        image_url = None

        return name, description, image_url

    except requests.exceptions.Timeout:
        return None, "❌ API 連線超時，請稍後再試！", None
    except requests.exceptions.RequestException as e:
        return None, f"❌ API 請求錯誤: {str(e)}", None

# 📌 Google Knowledge Graph 查詢 API
def query_google_kg(keyword, api_key):
    try:
        url = f"https://kgsearch.googleapis.com/v1/entities:search?query={keyword}&key={api_key}&limit=1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if "itemListElement" in data and len(data["itemListElement"]) > 0:
            entity = data["itemListElement"][0]["result"]
            name = entity.get("name", "無資料")
            description = entity.get("description", "無描述")
            image_url = entity.get("image", {}).get("contentUrl", None)

            return name, description, image_url
        else:
            return None, "⚠️ Google 知識圖譜沒有找到該關鍵字，請更換名稱！", None

    except requests.exceptions.Timeout:
        return None, "❌ Google API 連線超時，請稍後再試！", None
    except requests.exceptions.RequestException as e:
        return None, f"❌ Google API 請求錯誤: {str(e)}", None

# 📌 統一 API 查詢接口
def search_knowledge_graph(keyword, api_source, lang="en", google_api_key=None):
    if not keyword:
        return None, "⚠️ 請輸入查詢關鍵字！", None

    if api_source == "Wikidata":
        return query_wikidata(keyword, lang)
    elif api_source == "DBpedia":
        return query_dbpedia(keyword)
    elif api_source == "Google Knowledge Graph":
        if not google_api_key:
            return None, "❌ Google API Key 未設置！", None
        return query_google_kg(keyword, google_api_key)
    else:
        return None, "❌ 未知的 API 來源", None
