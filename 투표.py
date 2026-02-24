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

# ─── CSS 스타일링 ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.main-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FF6B35, #F7931E, #FF4E50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}

.sub-title {
    text-align: center;
    color: #888;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.restaurant-card {
    background: linear-gradient(145deg, #1a1a2e, #16213e);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid #2a2a4a;
    transition: all 0.3s ease;
    min-height: 420px;
}

.restaurant-card:hover {
    border-color: #FF6B35;
    box-shadow: 0 8px 32px rgba(255, 107, 53, 0.15);
}

.restaurant-name {
    font-size: 1.4rem;
    font-weight: 700;
    color: #FF6B35;
    margin-bottom: 0.3rem;
}

.restaurant-category {
    display: inline-block;
    background: rgba(255, 107, 53, 0.15);
    color: #FF8C5A;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    margin-bottom: 0.8rem;
}

.restaurant-desc {
    color: #ccc;
    font-size: 0.9rem;
    line-height: 1.6;
    margin-bottom: 1rem;
}

.menu-item {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: #ddd;
    font-size: 0.88rem;
}

.menu-name {
    color: #eee;
    font-weight: 500;
}

.menu-price {
    color: #F7931E;
    font-weight: 700;
    white-space: nowrap;
}

.menu-header {
    color: #FF6B35;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
    padding-bottom: 4px;
    border-bottom: 2px solid #FF6B35;
}

.vote-result-bar {
    background: linear-gradient(90deg, #FF6B35, #F7931E);
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    padding-left: 12px;
    color: white;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 6px;
    transition: width 0.5s ease;
}

.vote-count {
    font-size: 1.8rem;
    font-weight: 900;
    color: #FF6B35;
    text-align: center;
}

.note-tag {
    display: inline-block;
    background: rgba(255, 78, 80, 0.15);
    color: #FF4E50;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    margin-left: 4px;
}

.link-btn {
    display: inline-block;
    background: rgba(3, 199, 90, 0.12);
    color: #03C75A;
    padding: 4px 12px;
    border-radius: 8px;
    font-size: 0.8rem;
    text-decoration: none;
    margin-top: 8px;
}

.link-btn:hover {
    background: rgba(3, 199, 90, 0.25);
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #333, transparent);
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─── 식당 데이터 ───
RESTAURANTS = [
    {
        "id": 1,
        "name": "만원수산 정자점",
        "category": "🐟 생선회",
        "description": "정자역 인근 생선회 전문점. ★4.71 · 방문자 리뷰 348 · 블로그 리뷰 204. 합리적인 가격에 즐기는 신선한 회! 배달 주문도 가능합니다.",
        "note": "⭐ 4.71점",
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
        "category": "🥩 한식 · 삼겹살",
        "description": "방문자 리뷰 325 · 블로그 리뷰 386. 볶음밥으로 마무리하는 완벽한 식사! 호일 위에서 구워먹는 20대의 추억이 담긴 삼겹살 맛집입니다.",
        "note": None,
        "link": "https://map.naver.com/p/entry/place/1016077738?placePath=%2Fhome",
        "menus": [
            ("급냉삼겹살", "15,000원"),
            ("급냉목살", "16,000원"),
            ("생삼겹살", "가격 확인 필요"),
            ("볶음밥", "별도"),
        ]
    },
    {
        "id": 3,
        "name": "냉삼 전문점",
        "category": "🥓 냉삼",
        "description": "냉동 숙성 삼겹살 전문점. 냉동 숙성 과정을 거쳐 육즙이 풍부하고 부드러운 삼겹살을 즐길 수 있습니다. 단, 정자역에서 다소 거리가 있습니다.",
        "note": "⚠️ 거리가 멀어요!",
        "link": "https://map.naver.com/p/entry/place/1198189212?placePath=%2Fhome",
        "menus": [
            ("냉삼 세트 (2인)", "38,000원"),
            ("냉삼 (1인분)", "17,000원"),
            ("차돌박이", "18,000원"),
            ("물냉면", "8,000원"),
            ("비빔냉면", "8,000원"),
        ]
    },
    {
        "id": 4,
        "name": "피어39회",
        "category": "🐟 회",
        "description": "정자역 3번출구 도보 3분, 분당 정자동 가성비 횟집. 통영 직송 싱싱한 활어회를 합리적 가격에 즐길 수 있으며, 모듬회 세트부터 물회·해산물·매운탕까지 메뉴가 다양합니다. 다이닝코드 맛 4.4점의 인정받은 맛집!",
        "note": None,
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
        "category": "🐷 족발·보쌈",
        "description": "서울 3대 족발, 9년 연속 미쉐린 가이드 빕구르망 선정! 오향을 사용해 비린내를 잡은 부드럽고 촉촉한 족발이 대표 메뉴입니다. 열판 위에 따뜻하게 유지되어 끝까지 맛있게 즐길 수 있으며, 서비스 떡만둣국도 인기입니다.",
        "note": "🏅 미쉐린 빕구르망",
        "link": "https://naver.me/5D3t2nlL",
        "menus": [
            ("만족오향족발 (중)", "39,000원"),
            ("만족오향족발 (대)", "44,000원"),
            ("직화불족발 (중)", "41,000원"),
            ("반반족발 (중)", "42,000원"),
            ("냉채족발 (중)", "38,000원"),
            ("족발+보쌈 세트 (중)", "44,000원"),
            ("쟁반국수", "13,000원"),
        ]
    },
    {
        "id": 6,
        "name": "소소객잔 분당정자점",
        "category": "🥡 중화요리",
        "description": "정자역 도보 5분, 새로 오픈한 감성 중화주점. 붉은 조명에 동양풍 인테리어가 매력적인 곳으로, 무협지 분위기 속에서 다양한 중화요리와 술을 즐기기 좋습니다. 다이닝코드 평점 4.5의 떠오르는 맛집!",
        "note": "🆕 신규 오픈",
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

# ─── 투표 데이터 저장/로드 ───
VOTE_FILE = "votes.json"

def load_votes():
    if os.path.exists(VOTE_FILE):
        with open(VOTE_FILE, "r") as f:
            return json.load(f)
    return {"votes": {str(r["id"]): 0 for r in RESTAURANTS}, "voters": {}}

def save_votes(data):
    with open(VOTE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False)

# ─── 메인 UI ───
st.markdown('<div class="main-title">🍽️ 회식 맛집 투표</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">최대 2곳까지 선택 가능 · 분당 정자역 인근 맛집 6곳</div>', unsafe_allow_html=True)

# 투표 데이터 로드
vote_data = load_votes()

# ─── 탭 구성 ───
tab1, tab2 = st.tabs(["🗳️ 투표하기", "📊 결과보기"])

# ─── 투표 탭 ───
with tab1:
    # 이름 입력
    voter_name = st.text_input("🙋 이름을 입력하세요", placeholder="예: 홍길동", key="voter_name")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 식당 카드 3열 표시
    cols_row1 = st.columns(3)
    cols_row2 = st.columns(3)
    all_cols = cols_row1 + cols_row2
    
    for idx, restaurant in enumerate(RESTAURANTS):
        with all_cols[idx]:
            # 카드 시작
            note_html = ""
            if restaurant["note"]:
                note_html = f'<span class="note-tag">{restaurant["note"]}</span>'
            
            menu_html = ""
            for menu_name, menu_price in restaurant["menus"]:
                menu_html += f'''
                <div class="menu-item">
                    <span class="menu-name">{menu_name}</span>
                    <span class="menu-price">{menu_price}</span>
                </div>'''
            
            st.markdown(f'''
            <div class="restaurant-card">
                <div class="restaurant-name">{restaurant["name"]} {note_html}</div>
                <span class="restaurant-category">{restaurant["category"]}</span>
                <div class="restaurant-desc">{restaurant["description"]}</div>
                <div class="menu-header">📋 대표 메뉴</div>
                {menu_html}
                <a href="{restaurant["link"]}" target="_blank" class="link-btn">📍 네이버 지도에서 보기</a>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 투표 선택
    st.markdown("### 🗳️ 가고 싶은 곳을 선택하세요 (최대 2곳)")
    
    options = [f"{r['id']}. {r['name']}" for r in RESTAURANTS]
    selected = st.multiselect(
        "식당을 선택하세요",
        options=options,
        max_selections=2,
        placeholder="최대 2곳까지 선택 가능합니다",
        label_visibility="collapsed"
    )
    
    # 투표 버튼
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("🗳️ 투표하기!", use_container_width=True, type="primary"):
            if not voter_name.strip():
                st.error("이름을 입력해주세요!")
            elif len(selected) == 0:
                st.error("최소 1곳을 선택해주세요!")
            elif voter_name.strip() in vote_data.get("voters", {}):
                st.warning(f"'{voter_name.strip()}' 님은 이미 투표하셨습니다! 결과 탭에서 확인해주세요.")
            else:
                # 투표 처리
                selected_ids = [s.split(".")[0] for s in selected]
                for sid in selected_ids:
                    vote_data["votes"][sid] = vote_data["votes"].get(sid, 0) + 1
                
                vote_data["voters"][voter_name.strip()] = {
                    "selected": selected_ids,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_votes(vote_data)
                
                selected_names = [s.split(". ", 1)[1] for s in selected]
                st.success(f"🎉 {voter_name.strip()} 님의 투표가 완료되었습니다! → {', '.join(selected_names)}")
                st.balloons()

# ─── 결과 탭 ───
with tab2:
    # 최신 데이터 다시 로드
    vote_data = load_votes()
    
    total_votes = sum(vote_data["votes"].values())
    total_voters = len(vote_data.get("voters", {}))
    
    st.markdown(f"### 📊 현재 투표 현황")
    
    metric_cols = st.columns(3)
    with metric_cols[0]:
        st.metric("👥 총 참여자 수", f"{total_voters}명")
    with metric_cols[1]:
        st.metric("🗳️ 총 투표 수", f"{total_votes}표")
    with metric_cols[2]:
        # 1위 찾기
        if total_votes > 0:
            max_id = max(vote_data["votes"], key=vote_data["votes"].get)
            winner = next(r for r in RESTAURANTS if str(r["id"]) == max_id)
            st.metric("🏆 현재 1위", winner["name"])
        else:
            st.metric("🏆 현재 1위", "아직 없음")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 결과 바 차트
    sorted_restaurants = sorted(RESTAURANTS, key=lambda r: vote_data["votes"].get(str(r["id"]), 0), reverse=True)
    max_votes = max(vote_data["votes"].values()) if total_votes > 0 else 1
    
    for r in sorted_restaurants:
        rid = str(r["id"])
        count = vote_data["votes"].get(rid, 0)
        pct = (count / total_votes * 100) if total_votes > 0 else 0
        bar_width = max((count / max_votes * 100), 5) if max_votes > 0 else 5
        
        rank_emoji = ""
        if count > 0:
            rank = [str(rr["id"]) for rr in sorted_restaurants].index(rid) + 1
            if rank == 1: rank_emoji = "🥇 "
            elif rank == 2: rank_emoji = "🥈 "
            elif rank == 3: rank_emoji = "🥉 "
        
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 700; color: #eee; font-size: 1rem;">{rank_emoji}{r['name']}</span>
                <span style="color: #F7931E; font-weight: 700;">{count}표 ({pct:.0f}%)</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); border-radius: 8px; overflow: hidden; height: 28px;">
                <div style="width: {bar_width}%; background: linear-gradient(90deg, #FF6B35, #F7931E); height: 100%; border-radius: 8px; transition: width 0.5s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 투표자 목록
    if vote_data.get("voters"):
        st.markdown("### 📝 투표자 명단")
        for name, info in vote_data["voters"].items():
            selected_names = []
            for sid in info["selected"]:
                r = next((r for r in RESTAURANTS if str(r["id"]) == sid), None)
                if r:
                    selected_names.append(r["name"])
            st.markdown(f"- **{name}** → {', '.join(selected_names)} _{info.get('time', '')}_")
    
    # 초기화 버튼
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    with st.expander("⚙️ 관리자 도구"):
        if st.button("🗑️ 투표 초기화", type="secondary"):
            reset_data = {"votes": {str(r["id"]): 0 for r in RESTAURANTS}, "voters": {}}
            save_votes(reset_data)
            st.success("투표가 초기화되었습니다!")
            st.rerun()
