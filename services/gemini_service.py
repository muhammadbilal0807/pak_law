import os
import time
import random
import streamlit as st
from google import genai
from google.genai import types
from config.settings import PRIMARY_MODEL, FALLBACK_MODEL

@st.cache_resource
def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Secrets.")
        st.stop()
    return genai.Client(api_key=api_key)

def get_system_instruction(mode: str) -> str:
    if mode == "Legal Q&A":
        return """You are Pak Law AI, an authoritative legal assistant for Pakistan.
Keep answers under 250 words. Be concise.
Format with:
### 📌 Executive Legal Summary
### 📜 Applicable Laws (Cite PPC, CrPC, PECA, etc.)
### 🛠️ Key Legal Steps
### ⚖️ Consult an Advocate"""
    
    doc_name = mode.replace("Draft ", "")
    return f"""You are an expert Pakistani lawyer. The user wants you to draft a {doc_name}.
Provide a professional, fill-in-the-blank template following standard Pakistani legal
drafting conventions. Use brackets [Like This] for missing information. Keep it strictly
relevant to Pakistan, and end with one line noting this is a draft for review by a
licensed advocate before use."""

def call_gemini_with_retry(client, contents, system_instruction, max_output_tokens, max_retries=3, thinking_level="LOW"):
    models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]
    last_error = None
    token_budget = max_output_tokens

    for model_name in models_to_try:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        max_output_tokens=token_budget,
                        thinking_config=types.ThinkingConfig(thinking_level=thinking_level),
                    ),
                )

                finish_reason = ""
                if response.candidates:
                    finish_reason = str(response.candidates[0].finish_reason)
                text = getattr(response, "text", None)

                if "MAX_TOKENS" in finish_reason:
                    token_budget = min(token_budget * 2, 4096)
                    time.sleep(0.3)
                    continue

                if not text or not text.strip():
                    raise ValueError("empty_response")
                return text, model_name

            except Exception as e:
                last_error = e
                msg = str(e).lower()

                if "429" in msg or "resource_exhausted" in msg or "rate limit" in msg or "quota" in msg:
                    time.sleep((2 ** attempt) + random.random())
                    continue
                if "404" in msg or "not_found" in msg or "not found" in msg:
                    break
                if "empty_response" in msg:
                    time.sleep(0.5)
                    continue
                time.sleep(1)
                break

    raise RuntimeError(f"All models failed. Last error: {last_error}")