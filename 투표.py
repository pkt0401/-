import streamlit as st
import json
import os
from datetime import datetime

# ─── 페이지 설정 ───
st.set_page_config(
    page_title="🍽️ 회식 맛집 투표",
    page_icon="🗳️",
    layout="wide",
)

# ─── 식당 데이터 ───
RESTAURANTS = [
    {
        "id": 1,
        "name": "만원수산 정자점",
        "emoji": "🐟",
        "category": "생선회",
        "description": "★4.71 · 리뷰 348 · 합리적인 가격에 즐기는 신선한 회! 배달 주문도 가능합니다.",
        "note": "",
        "link": "https://map.naver.com/p/entry/place/1954161640?placePath=%2Fhome",
        "menus": [
            ("삼만이(광어+도다리+연어) 2~3인", "39,000원"),
            ("만만이(광어+도다리)", "29,000원"),
            ("모듬회 (중)", "49,000원"),
            ("모듬회 (대)", "69,000원"),
            ("매운탕", "10,000원"),
        ]
    },
    {
        "id": 2,
        "name": "은박집",
        "emoji": "🥩",
        "category": "한식 · 삼겹살",
        "description": "리뷰 325 · 블로그 386 · 볶음밥으로 마무리하는 완벽한 식사! 호일 위에서 구워먹는 추억의 삼겹살.",
        "note": "",
        "link": "https://map.naver.com/p/entry/place/1016077738?placePath=%2Fhome",
        "menus": [
            ("급냉삼겹살", "15,000원"),
            ("급냉목살", "16,000원"),
            ("생삼겹살", "가격 문의"),
            ("볶음밥", "서비스"),
        ]
    },
    {
        "id": 3,
        "name": "냉삼 전문점",
        "emoji": "🥓",
        "category": "냉삼",
        "description": "냉동 숙성 과정을 거쳐 육즙이 풍부하고 부드러운 삼겹살을 즐길 수 있는 전문점.",
        "note": "⚠️ 거리가 멀어요!",
        "link": "https://map.naver.com/p/entry/place/1198189212?placePath=%2Fhome",
        "menus": [
            ("냉삼 세트 (2인)", "38,000원"),
            ("냉삼 (1인분)", "17,000원"),
            ("차돌박이", "18,000원"),
            ("물냉면 / 비빔냉면", "8,000원"),
        ]
    },
    {
        "id": 4,
        "name": "피어39회",
        "emoji": "🐟",
        "category": "회",
        "description": "정자역 3번출구 도보 3분 · 다이닝코드 맛 4.4점 · 통영 직송 가성비 횟집. 모듬회부터 물회·매운탕까지!",
        "note": "",
        "link": "https://naver.me/GWrye4jr",
        "menus": [
            ("모듬회 (소)", "49,000원"),
            ("광어+연어(or 우럭) 세트", "49,000원"),
            ("제주산 대방어회", "59,000원"),
            ("왕새우소금구이 500g", "39,000원"),
            ("해물라면", "15,000원"),
            ("매운탕", "10,000원"),
        ]
    },
    {
        "id": 5,
        "name": "만족오향족발 정자점",
        "emoji": "🐷",
        "category": "족발·보쌈",
        "description": "서울 3대 족발 · 9년 연속 미쉐린 빕구르망! 오향으로 비린내 잡은 촉촉한 족발. 열판으로 끝까지 따뜻하게!",
        "note": "🏅 미쉐린",
        "link": "https://naver.me/5D3t2nlL",
        "menus": [
            ("만족오향족발 (중)", "39,000원"),
            ("만족오향족발 (대)", "44,000원"),
            ("직화불족발 (중)", "41,000원"),
            ("반반족발 (중)", "42,000원"),
            ("족발+보쌈 세트 (중)", "44,000원"),
            ("쟁반국수", "13,000원"),
        ]
    },
    {
        "id": 6,
        "name": "소소객잔 분당정자점",
        "emoji": "🥡",
        "category": "중화요리",
        "description": "정자역 도보 5분 · 다이닝코드 4.5점 · 붉은 조명 동양풍 감성 중화주점. 회식·술자리에 딱!",
        "note": "🆕 신규",
        "link": "https://naver.me/Gj6BE7iH",
        "menus": [
            ("꿔바로우", "18,000원"),
            ("마라샹궈 (2인)", "32,000원"),
            ("탕수육 (중)", "22,000원"),
            ("짬뽕", "10,000원"),
            ("짜장면", "9,000원"),
            ("볶음밥", "10,000원"),
        ]
    },
]

# ─── 투표 데이터 ───
VOTE_FILE = "votes.json"

def load_votes():
    if os.path.exists(VOTE_FILE):
        with open(VOTE_FILE, "r") as f:
            return json.load(f)
    return {"votes": {str(r["id"]): 0 for r in RESTAURANTS}, "voters": []}

def save_votes(data):
    with open(VOTE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False)

# ─── 헤더 ───
st.markdown("## 🍽️ 회식 맛집 투표")
st.caption("최대 **2곳**까지 선택 가능 · 분당 정자역 인근 맛집 6곳")
st.divider()

vote_data = load_votes()
tab1, tab2 = st.tabs(["🗳️ 투표하기", "📊 결과보기"])

# ━━━━━━━━━━━━━━━ 투표 탭 ━━━━━━━━━━━━━━━
with tab1:
    for row_start in range(0, 6, 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            idx = row_start + i
            if idx >= len(RESTAURANTS):
                break
            r = RESTAURANTS[idx]
            with col:
                with st.container(border=True):
                    note_str = f"  {r['note']}" if r['note'] else ""
                    st.subheader(f"{r['emoji']} {r['name']}{note_str}")
                    st.caption(f"📂 {r['category']}")
                    st.write(r["description"])

                    with st.expander("📋 대표 메뉴 보기"):
                        for menu_name, menu_price in r["menus"]:
                            c1, c2 = st.columns([3, 1.2])
                            c1.markdown(f"**{menu_name}**")
                            c2.markdown(f"`{menu_price}`")

                    st.link_button("📍 네이버 지도", r["link"], use_container_width=True)

    st.divider()
    st.markdown("### 🗳️ 가고 싶은 곳을 선택하세요!")

    options = [f"{r['emoji']} {r['name']}" for r in RESTAURANTS]
    selected = st.multiselect(
        "식당 선택 (최대 2곳)",
        options=options,
        max_selections=2,
        placeholder="여기를 눌러 최대 2곳을 선택하세요",
    )

    if st.button("🗳️ 투표하기!", use_container_width=True, type="primary"):
        if len(selected) == 0:
            st.error("최소 1곳을 선택해주세요!")
        else:
            for sel in selected:
                for r in RESTAURANTS:
                    if sel == f"{r['emoji']} {r['name']}":
                        vote_data["votes"][str(r["id"])] = vote_data["votes"].get(str(r["id"]), 0) + 1
            vote_data["voters"].append({
                "selected": selected,
                "time": datetime.now().strftime("%m/%d %H:%M")
            })
            save_votes(vote_data)
            st.success(f"🎉 투표 완료! → **{', '.join(selected)}**")
            st.balloons()

# ━━━━━━━━━━━━━━━ 결과 탭 ━━━━━━━━━━━━━━━
with tab2:
    vote_data = load_votes()
    total_votes = sum(vote_data["votes"].values())
    total_voters = len(vote_data.get("voters", []))

    m1, m2, m3 = st.columns(3)
    m1.metric("👥 참여자", f"{total_voters}명")
    m2.metric("🗳️ 총 투표", f"{total_votes}표")
    if total_votes > 0:
        max_id = max(vote_data["votes"], key=vote_data["votes"].get)
        winner = next(r for r in RESTAURANTS if str(r["id"]) == max_id)
        m3.metric("🏆 1위", f"{winner['emoji']} {winner['name']}")
    else:
        m3.metric("🏆 1위", "아직 없음")

    st.divider()

    sorted_rs = sorted(RESTAURANTS, key=lambda r: vote_data["votes"].get(str(r["id"]), 0), reverse=True)

    for rank, r in enumerate(sorted_rs, 1):
        rid = str(r["id"])
        count = vote_data["votes"].get(rid, 0)
        pct = (count / total_votes * 100) if total_votes > 0 else 0
        medal = ""
        if count > 0:
            if rank == 1: medal = "🥇 "
            elif rank == 2: medal = "🥈 "
            elif rank == 3: medal = "🥉 "

        c1, c2, c3 = st.columns([3, 6, 1.5])
        c1.markdown(f"**{medal}{r['emoji']} {r['name']}**")
        c2.progress(pct / 100 if total_votes > 0 else 0)
        c3.markdown(f"**{count}표** ({pct:.0f}%)")

    st.divider()

    if vote_data.get("voters"):
        with st.expander(f"📝 투표 기록 ({total_voters}건)"):
            for i, v in enumerate(reversed(vote_data["voters"]), 1):
                st.write(f"{i}. {', '.join(v['selected'])} — _{v.get('time', '')}_")

    with st.expander("⚙️ 관리자"):
        if st.button("🗑️ 투표 초기화"):
            save_votes({"votes": {str(r["id"]): 0 for r in RESTAURANTS}, "voters": []})
            st.success("초기화 완료!")
            st.rerun()
