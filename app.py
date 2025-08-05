import streamlit as st

# openai 라이브러리 임포트 (app.py 상단에서 import 필요)
from openai import OpenAI

# Upstage Solar Pro 2 API 클라이언트 설정
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    base_url="https://api.upstage.ai/v1"
)

st.title("🧑‍🎓 학생 심리 상담 챗봇 (Solar Pro 2)")

st.write(
    """
    안녕하세요! 이 챗봇은 학생 여러분의 고민, 감정, 심리상담을 위해 준비되었습니다.
    편하게 고민을 남겨주세요. 🤗
    """
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 무엇이든 편하게 말씀해 주세요. 여러분의 이야기를 들어드릴게요."}
    ]

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("고민이나 감정을 입력해 주세요."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Upstage Solar Pro 2로 메시지 전송 (스트리밍)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # 이전 대화 이력도 함께 전달
        upstage_messages = [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]

        stream = client.chat.completions.create(
            model="solar-pro2",
            messages=upstage_messages,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
