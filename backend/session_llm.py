from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
import re,os

load_dotenv()
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.1,
    timeout=40
)

# -------- CLEAN TEXT ----------
def clean_text(text: str):
    text = text.strip()
    text = re.sub(r"^Here.*?:", "", text, flags=re.IGNORECASE)
    return text.strip()


# -------- TITLE --------
title_prompt = ChatPromptTemplate.from_messages([
    ("system", "Generate ONLY a short 5-word legal topic title. No explanation."),
    ("human", "{question}")
])

async def generate_title(question: str):
    chain = title_prompt | llm
    res = await chain.ainvoke({"question": question})
    return clean_text(res.content)[:60]


# -------- SUMMARY --------
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", """
Update conversation summary.

Rules:
- Max 7 lines
- Clear and structured
- No explanation text
"""),
    ("human", """
Previous summary:
{summary}

New question:
{question}

Assistant response:
{answer}

Return updated summary only.
""")
])

async def generate_summary(summary, question, answer):
    chain = summary_prompt | llm
    res = await chain.ainvoke({
        "summary": summary or "",
        "question": question,
        "answer": answer
    })

    return clean_text(res.content)