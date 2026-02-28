from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def get_llm_response(input_text: str, expert_type: str) -> str:
	if expert_type.startswith("A"):
		system_prompt = (
			"あなたは旅行プランニングの専門家です。"
			"目的地、予算、日数を踏まえて、実行しやすい提案をわかりやすく日本語で回答してください。"
		)
	else:
		system_prompt = (
			"あなたはPythonプログラミング学習の専門家です。"
			"初心者にもわかるように、手順と理由を簡潔に日本語で説明してください。"
		)

	llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
	messages = [
		SystemMessage(content=system_prompt),
		HumanMessage(content=input_text),
	]
	result = llm.invoke(messages)
	return result.content


st.title("かんたん相談アプリ")

st.write("##### アプリ概要")
st.write("このアプリは、入力した相談内容に対してAIがわかりやすく回答するアプリです。")
st.write("旅行の相談か、Python学習の相談かを選んで使えます。")
st.write("##### 操作方法")
st.write("1. まず、相談したいジャンルを選びます。")
st.write("2. 次に、相談したい内容を入力欄に書きます。")
st.write("3. 最後に「回答を見る」を押すと、AIの回答が表示されます。")

selected_expert = st.radio(
	"相談ジャンルを選んでください。",
	["A: 旅行の相談", "B: Python学習の相談"],
)

st.divider()

input_message = st.text_input(
	label="相談内容を入力してください。"
)
st.write("相談例（A: 旅行の相談）: 3日間で大阪を楽しむ旅行プランを知りたい")
st.write("相談例（B: Python学習の相談）: Pythonのfor文とwhile文の違いを、初心者向けに教えてほしい")

if st.button("回答を見る"):
	st.divider()

	if input_message:
		try:
			response = get_llm_response(input_message, selected_expert)
			st.write("##### AIからの回答")
			st.write(response)
		except Exception:
			st.error("回答の取得に失敗しました。時間をおいて、もう一度お試しください。")
	else:
		st.error("相談内容を入力してから「回答を見る」を押してください。")
