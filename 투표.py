import streamlit as st

# 1. 페이지 기본 설정 (가장 먼저 와야 함)
st.set_page_config(page_title="팀 모임 장소 투표", page_icon="🍻", layout="wide")

# 2. 커스텀 CSS (제목 및 UI 다듬기)
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 800;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown('<p class="main-title">🍻 팀 모임/회식 장소 투표</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">우리의 즐거운 시간을 위해! 가장 끌리는 메뉴 2가지를 선택해주세요.</p>', unsafe_allow_html=True)
st.divider()

# 음식점 데이터 (이미지에서 추출한 정보 반영 완료)
restaurants = [
    {
        "id": 1, 
        "name": "만원수산 정자점", 
        "url": "https://map.naver.com/p/entry/place/1954161640", 
        "desc": "합리적인 가격에 즐기는 신선한 회! (별점 4.71)", 
        "menu": "• 삼만이(광어+도다리+연어) : 39,000원\n• 만만이(광어+도다리) : 29,000원", 
        "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80"
    },
    {
        "id": 2, 
        "name": "은박집", 
        "url": "https://map.naver.com/p/entry/place/1016077738", 
        "desc": "20대의 추억이 담긴 호일 위 냉동 삼겹살 (볶음밥 필수!)", 
        "menu": "• 급냉삼겹살 : 15,000원\n• 급냉목살 : 16,000원", 
        "img": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&q=80"
    },
    {
        "id": 3, 
        "name": "냉동 삼겹살 전문점 (3번 후보)", 
        "url": "https://map.naver.com/p/entry/place/1198189212", 
        "desc": "지글지글 고소한 냉삼! (다소 거리가 멀 수 있어요)", 
        "menu": "• 냉동삼겹살 : 00,000원\n• 볶음밥 : 0,000원", 
        "img": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=500&q=80"
    },
    {
        "id": 4, 
        "name": "피어39회", 
        "url": "https://naver.me/GWrye4jr", 
        "desc": "정자역 인근! 신선한 숙성회 및 해산물 전문점", 
        "menu": "• 모듬추천사시미 : 59,000원\n• 도다리+광어/우럭 : 49,000원", 
        "img": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=500&q=80"
    },
    {
        "id": 5, 
        "name": "만족오향족발 정자점", 
        "url": "https://naver.me/5D3t2nlL", 
        "desc": "서울 3대 족발! 부드럽고 따뜻한 족발과 보쌈", 
        "menu": "• 만족오향족발(중) : 38,000원\n• 보쌈(중) : 35,000원", 
        "img": "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?w=500&q=80"
    },
    {
        "id": 6, 
        "name": "소소객잔 분당정자점", 
        "url": "https://naver.me/Gj6BE7iH", 
        "desc": "분위기 좋은 퓨전 중식 주점 (느티로51번길)", 
        "menu": "• 깐풍기 / 유린기 / 짬뽕탕 등\n(가격은 링크 참조)", 
        "img": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=500&q=80"
    }
]

# 3. 카드형 레이아웃 구성 (3열 x 2행)
cols = st.columns(3)

for idx, r in enumerate(restaurants):
    col = cols[idx % 3] # 3개씩 나열하기 위함
    with col:
        with st.container(border=True):
            st.image(r["img"], use_container_width=True)
            st.subheader(f"{r['id']}. {r['name']}")
            st.caption(r["desc"])
            
            with st.expander("🍽️ 메뉴 및 가격 보기"):
                st.write(r["menu"])
                
            st.markdown(f"[📍 네이버 지도에서 보기]({r['url']})")

st.divider()

# 4. 투표 섹션 레이아웃
st.subheader("🗳️ 당신의 선택은?")
st.info("💡 최고의 장소를 골라주세요! (최대 2개)")

options = [r["name"] for r in restaurants]

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    selected_places = st.multiselect(
        "가장 가고 싶은 식당 (최대 2개 선택):",
        options=options,
        max_selections=2,
        placeholder="여기를 눌러 후보를 선택하세요 👇"
    )

    if st.button("🚀 투표 제출하기", use_container_width=True, type="primary"):
        if len(selected_places) == 0:
            st.error("앗! 최소 1개의 식당은 선택해 주셔야 해요. 😅")
        else:
            st.balloons()
            st.success("🎉 투표가 성공적으로 완료되었습니다!")
            
            st.markdown("### ✅ 나의 픽")
            for place in selected_places:
                st.markdown(f"- **{place}**")
