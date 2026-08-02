import streamlit as st
from services.prompt_ai_service import get_all_prompts, update_prompt_template, save_system_setting, get_system_setting
from services.admin_service import log_audit_action
from config.settings import DEFAULT_AI_CONFIG

def render_admin_prompts_ai(conn):
    st.markdown('<div class="admin-header">Prompts & AI System Configurations</div>', unsafe_allow_html=True)
    st.markdown('<div class="admin-subheader">Tune Gemini model parameters, adjust temperatures, and version legal system prompts dynamically.</div>', unsafe_allow_html=True)

    tab_p, tab_ai = st.tabs(["📝 Prompt Template Manager", "🎛️ Gemini Model Settings"])

    with tab_p:
        df_prompts = get_all_prompts(conn)
        st.dataframe(df_prompts, use_container_width=True, hide_index=True)
        
        st.markdown("### Update Prompt")
        prompt_name = st.text_input("Template Name", value="Default Legal Assistant")
        current_prompt = st.text_area("System Instruction Context", value="You are an expert Pakistani Legal Assistant specializing in Constitution, CrPC, PPC, and PECA.", height=150)
        
        if st.button("Publish New Prompt Version", type="primary"):
            update_prompt_template(conn, prompt_name, current_prompt)
            log_audit_action(conn, st.session_state.user["id"], "UPDATE_PROMPT", f"Updated template: {prompt_name}")
            st.success("Prompt version updated successfully.")
            st.rerun()

    with tab_ai:
        st.markdown("### 🤖 Model Hyperparameters")
        col1, col2 = st.columns(2)
        
        with col1:
            current_model = get_system_setting(conn, "ai_model", DEFAULT_AI_CONFIG["model_name"])
            model_choice = st.selectbox("Gemini Model Engine", ["gemini-2.5-flash", "gemini-2.5-pro"], index=0)
            
            curr_temp = float(get_system_setting(conn, "ai_temperature", DEFAULT_AI_CONFIG["temperature"]))
            temp_choice = st.slider("Temperature (Creativity vs Determinism)", 0.0, 1.0, curr_temp, 0.05)
            
        with col2:
            curr_tokens = int(get_system_setting(conn, "ai_max_tokens", DEFAULT_AI_CONFIG["max_tokens"]))
            max_tokens_choice = st.number_input("Max Token Output Limit", min_value=512, max_value=8192, value=curr_tokens, step=256)
            
        if st.button("Save Model Configurations", type="primary"):
            save_system_setting(conn, "ai_model", model_choice)
            save_system_setting(conn, "ai_temperature", temp_choice)
            save_system_setting(conn, "ai_max_tokens", max_tokens_choice)
            log_audit_action(conn, st.session_state.user["id"], "UPDATE_AI_CONFIG", f"Saved Model: {model_choice}, Temp: {temp_choice}")
            st.success("AI Configuration saved.")