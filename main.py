import streamlit as st
import google.generativeai as genai

# 設定網頁標題和圖示
st.set_page_config(page_title="易恩設計 - 智慧裝修顧問", page_icon="🏠", layout="wide")

# --- 側邊欄設定 (輸入區) ---
st.sidebar.title("🏠 易恩設計 - 裝修諮詢")
st.sidebar.write("請輸入您的需求，AI 總監將為您分析。")

# API Key 輸入欄位
api_key = st.sidebar.text_input("請輸入您的 Google API Key", type="password")

# 1. 選擇諮詢項目
project_type = st.sidebar.selectbox(
    "請問您想諮詢的項目是？",
    ["老屋/中古屋翻新", "新成屋裝潢", "辦公室/商業空間", "系統櫃/木工/局部裝修", "其他/特殊需求"]
)

# 2. 房屋地點 (新增下拉選單)
city_options = ["高雄市", "台南市", "台中市", "桃園市", "新北市", "台北市", "屏東縣", "其他地區"]
selected_city = st.sidebar.selectbox("房屋地點", city_options)

# 如果選其他，讓客戶手動輸入
if selected_city == "其他地區":
    location = st.sidebar.text_input("請輸入縣市名稱")
else:
    location = selected_city

# 3. 其他細節
size = st.sidebar.number_input("室內坪數", min_value=1, value=30)
house_age = st.sidebar.number_input("屋齡 (年)", min_value=0, value=0)
budget = st.sidebar.text_input("預計預算範圍 (選填)", placeholder="例如：200萬左右")
description = st.sidebar.text_area("需求描述 / 特殊備註", placeholder="例如：想要開放式廚房、有養貓、或是針對漏水問題...")

# --- 主畫面設定 ---
st.title("🏠 易恩設計 - AI 智慧裝修健檢報告")
st.write("👋 您好！我是易恩設計的 AI 裝修顧問。輸入左側資料，我將為您提供專業的施工建議與預算評估。")

# --- AI 分析邏輯 ---
if st.sidebar.button("🚀 開始分析"):
    if not api_key:
        st.error("⚠️ 請先在側邊欄貼上您的 Google API Key 才能運作喔！")
    else:
        try:
            # 設定 Google Gemini (使用最穩定的 pro 版本)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')

            # 組合給 AI 的指令 (Prompt)
            prompt = f"""
            你現在是【易恩室內裝修設計有限公司】的資深設計總監。
            你有 20 年的台灣在地裝修經驗，講話誠懇、專業，像是個老朋友給建議，不要太像機器人。
            
            客戶資料如下：
            - 諮詢項目：{project_type}
            - 地點：{location}
            - 坪數：{size} 坪
            - 屋齡：{house_age} 年
            - 預算：{budget}
            - 詳細需求：{description}

            請根據上述資料，給出一份專業的分析報告。內容必須包含：
            1. 【總監觀點】：針對客戶的屋齡和項目，給出最核心的建議（例如老屋要小心水電、辦公室要注意動線）。
            2. 【施工重點與風險】：列出 3-5 點該項目最需要注意的細節。
            3. 【預算粗估參考】：根據台灣南部行情，給出一個合理的預算區間概念，並說明錢主要會花在哪裡。
            4. 【結語】：溫暖的鼓勵。

            請用 Markdown 格式輸出，重點文字可以加粗。
            """

            with st.spinner("易恩總監正在思考您的案子，請稍等... 🏠"):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
                # --- 呼籲行動 (Call to Action) ---
                st.markdown("---")
                st.success("💡 喜歡這份專業建議嗎？裝修細節繁雜，建議直接與我們討論，避免踩雷！")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info("📞 預約專線：09XX-XXX-XXX") # 您的電話
                with col2:
                    st.warning("💬 點此加 Line 諮詢") # 您的 Line

        except Exception as e:
            st.error(f"發生錯誤：{e}\n建議：請檢查您的 API Key 是否正確，或是重新整理網頁。")

# --- 頁尾 ---
st.markdown("---")
st.caption("© 2025 易恩室內裝修設計有限公司 | AI 分析僅供參考，實際報價以現場丈量為準")
