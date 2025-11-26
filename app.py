import streamlit as st
import random

# --- Constants ---
MIN_NUM = 1
MAX_NUM = 200
GAME_TITLE = "🧠 1부터 200까지 숫자 맞히기 게임"

# --- Session State Initialization ---
# Streamlit 앱이 처음 로드될 때 또는 '재시작' 시에만 실행됩니다.
def initialize_game():
    """게임을 초기화하고 새로운 정답 숫자를 설정합니다."""
    st.session_state.secret_number = random.randint(MIN_NUM, MAX_NUM)
    st.session_state.attempts = 0
    st.session_state.message = "게임을 시작합니다! 숫자를 맞춰보세요."

if 'secret_number' not in st.session_state:
    initialize_game()

# --- Core Game Logic ---
def check_guess():
    """사용자의 추측을 확인하고 결과를 업데이트합니다."""
    # 1. 입력 유효성 검사 및 값 가져오기
    try:
        guess = st.session_state.current_guess
    except AttributeError:
        # st.number_input을 통해 guess 값을 가져오지 못했을 경우
        st.session_state.message = "⚠️ 숫자를 입력하고 '추측하기' 버튼을 눌러주세요."
        return
    
    # 입력 값이 None일 경우 처리 (Streamlit의 number_input이 None을 반환할 수 있음)
    if guess is None:
        st.session_state.message = "⚠️ 숫자를 입력해 주세요."
        return

    # 범위 확인
    if not (MIN_NUM <= guess <= MAX_NUM):
        st.session_state.message = f"⚠️ {MIN_NUM}부터 {MAX_NUM} 사이의 숫자를 입력해야 합니다."
        return
        
    st.session_state.attempts += 1
    
    # 2. 정답 비교 및 피드백 제공
    secret = st.session_state.secret_number
    
    if guess < secret:
        st.session_state.message = f"⬆️ {guess}는 정답보다 **더 큰** 숫자입니다!"
        st.session_state.status = "too_low"
    elif guess > secret:
        st.session_state.message = f"⬇️ {guess}는 정답보다 **더 작은** 숫자입니다!"
        st.session_state.status = "too_high"
    else:
        # 3. 정답을 맞힌 경우
        st.session_state.message = (
            f"🎉🎉 **축하합니다!** 🎉🎉\n\n"
            f"숨겨진 숫자는 **{secret}**가 맞습니다!\n"
            f"총 **{st.session_state.attempts}**번 만에 정답을 맞히셨습니다."
        )
        st.session_state.status = "correct"


# --- Streamlit UI Layout ---

st.set_page_config(page_title=GAME_TITLE, layout="centered")

st.title(GAME_TITLE)
st.markdown("정답을 맞힐 때까지 **무제한으로** 시도할 수 있습니다.")

# --- Current Attempts and Range Info ---
st.info(f"현재 시도 횟수: **{st.session_state.attempts}**회")
st.markdown(f"**범위:** `{MIN_NUM}` 부터 `{MAX_NUM}` 까지")

# 1. 사용자 입력 (st.number_input)
# key="current_guess"로 입력값을 st.session_state.current_guess에 저장합니다.
user_guess = st.number_input(
    "당신의 추측을 입력하세요:",
    min_value=MIN_NUM,
    max_value=MAX_NUM,
    step=1,
    key="current_guess",
    disabled=(st.session_state.get('status') == "correct") # 정답 맞히면 비활성화
)

# 2. 추측하기 버튼
# 버튼 클릭 시 check_guess 함수를 실행합니다.
st.button(
    "추측하기 (Guess)", 
    on_click=check_guess, 
    use_container_width=True,
    disabled=(st.session_state.get('status') == "correct") # 정답 맞히면 비활성화
)

# 3. 게임 피드백 출력
if st.session_state.message:
    # 정답을 맞혔을 경우 성공 메시지 출력
    if st.session_state.get('status') == "correct":
        st.balloons() # 축하 풍선 효과
        st.success(st.session_state.message)
    # 힌트 메시지 출력
    elif st.session_state.get('status') == "too_low" or st.session_state.get('status') == "too_high":
        st.warning(st.session_state.message)
    # 기타 정보/오류 메시지 출력
    else:
        st.info(st.session_state.message)

st.markdown("---")

# 4. 게임 재시작 버튼
st.button(
    "🔄 게임 재시작", 
    on_click=initialize_game, 
    use_container_width=True
)
