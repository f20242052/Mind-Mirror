import streamlit as st
from datetime import datetime

from backend.config import MOODS, MOOD_COLORS
import backend.auth as auth
import backend.diary as diary
import backend.ai as ai
import backend.analytics as analytics

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindMirror ✨",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: linear-gradient(135deg, #f0ebff 0%, #fce4ec 50%, #e8f4fd 100%);
    min-height: 100vh;
}
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(200,180,220,0.3);
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }
.mirror-card {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(8px);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(200,180,220,0.25);
    box-shadow: 0 4px 24px rgba(160,130,200,0.08);
    transition: box-shadow 0.2s ease;
}
.mirror-card:hover { box-shadow: 0 8px 32px rgba(160,130,200,0.15); }
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 600;
    color: #4a3060;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
}
.page-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: #9b84b0;
    margin-bottom: 1.8rem;
    font-weight: 300;
}
.entry-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: #3d2b52;
    margin: 0 0 0.3rem 0;
}
.entry-meta { font-size: 0.8rem; color: #b39cc7; margin-bottom: 0.7rem; }
.entry-preview { color: #5e4a72; font-size: 0.9rem; line-height: 1.6; margin-bottom: 0.8rem; }
.mood-pill {
    display: inline-block;
    padding: 0.2rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: #3d2b52;
}
.insight-box {
    background: linear-gradient(135deg, #f3eeff, #fce8f3);
    border-left: 4px solid #c9b1d9;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #4a3060;
    line-height: 1.7;
}
.reflection-box {
    background: linear-gradient(135deg, #e8f4fd, #f0ebff);
    border-left: 4px solid #a8dadc;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.9rem;
    color: #2d5a6b;
    font-style: italic;
    line-height: 1.7;
}
.theme-tag {
    display: inline-block;
    background: rgba(200,180,240,0.25);
    color: #6b4d90;
    border-radius: 999px;
    padding: 0.2rem 0.65rem;
    font-size: 0.75rem;
    margin: 0.2rem;
    border: 1px solid rgba(180,150,220,0.35);
}
.stat-card {
    background: rgba(255,255,255,0.85);
    border-radius: 16px;
    padding: 1.2rem 1rem;
    text-align: center;
    border: 1px solid rgba(200,180,220,0.2);
    box-shadow: 0 2px 12px rgba(160,130,200,0.07);
}
.stat-number { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 600; color: #6b4d90; }
.stat-label { font-size: 0.78rem; color: #b39cc7; margin-top: 0.2rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
.stButton > button { border-radius: 12px !important; font-family: 'Inter', sans-serif !important; font-weight: 500 !important; border: none !important; transition: all 0.2s ease !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #9b7ed4, #c06090) !important; color: white !important; }
.stButton > button[kind="primary"]:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    border-radius: 12px !important;
    border: 1.5px solid rgba(180,150,220,0.35) !important;
    font-family: 'Inter', sans-serif !important;
    background: rgba(255,255,255,0.95) !important;
    color: #1a1a2e !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder { color: #a89bbf !important; }
.stTextArea > div > div > textarea {
    font-family: 'Playfair Display', serif !important;
    font-size: 1rem !important;
    line-height: 1.8 !important;
    color: #1a1a2e !important;
}
.auth-tagline { color: #7a6090 !important; }
.page-subtitle { color: #7a6090 !important; }
.entry-meta { color: #7a6090 !important; }
hr { border-color: rgba(180,150,220,0.2) !important; }
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; background: transparent !important; }
.stTabs [data-baseweb="tab"] { border-radius: 12px !important; padding: 0.4rem 1.2rem !important; font-family: 'Inter', sans-serif !important; }
.stTabs [aria-selected="true"] { background: rgba(155,126,212,0.15) !important; color: #6b4d90 !important; }
.auth-logo { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 600; color: #4a3060; text-align: center; margin-bottom: 0.3rem; }
.auth-tagline { text-align: center; color: #9b84b0; font-size: 1rem; margin-bottom: 2rem; }
.lang-badge {
    display: inline-block;
    background: rgba(155,126,212,0.15);
    color: #6b4d90;
    border-radius: 999px;
    padding: 0.15rem 0.6rem;
    font-size: 0.75rem;
    margin-left: 0.4rem;
    border: 1px solid rgba(155,126,212,0.3);
}
</style>
""", unsafe_allow_html=True)


# ── Translation helpers ───────────────────────────────────────────────────────
LANGUAGES = ["English", "Hindi", "Telugu"]


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_translate(text: str, language: str) -> str:
    """Cache translations for 1 hour to avoid repeated Groq calls."""
    return ai.translate_text(text, language)


def t(text: str) -> str:
    """Translate text to the currently selected language."""
    lang = st.session_state.get("language", "English")
    if lang == "English":
        return text
    try:
        return _cached_translate(text, lang)
    except Exception:
        return text  # fall back to English if translation fails


# ── Session helpers ───────────────────────────────────────────────────────────
def is_logged_in():
    return "user" in st.session_state and st.session_state.user is not None


def current_user():
    return st.session_state.get("user")


def current_token():
    return st.session_state.get("access_token")


# ── Mood pill HTML ────────────────────────────────────────────────────────────
def mood_pill(mood: str) -> str:
    color = MOOD_COLORS.get(mood, "#C9B1D9")
    return f'<span class="mood-pill" style="background:{color}33; border:1px solid {color}66;">{mood}</span>'


# ── Auth pages ────────────────────────────────────────────────────────────────
def show_auth():
    # Language picker even before login
    lang_col1, lang_col2, lang_col3 = st.columns([3, 1, 3])
    with lang_col2:
        prev_lang = st.session_state.get("language", "English")
        lang = st.selectbox(
            "🌐",
            LANGUAGES,
            index=LANGUAGES.index(prev_lang),
            key="language",
            label_visibility="collapsed",
        )
        if lang != prev_lang:
            st.session_state.language = lang
            st.rerun()

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown('<div class="auth-logo">🪞 MindMirror</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="auth-tagline">{t("Your private space to reflect, grow, and understand yourself.")}</div>',
            unsafe_allow_html=True,
        )

        tab_login, tab_register = st.tabs([t("✨ Sign In"), t("🌱 Create Account")])

        with tab_login:
            with st.form("login_form"):
                st.markdown(f"#### {t('Welcome back')}")
                email = st.text_input(t("Email"), placeholder="you@example.com")
                password = st.text_input(t("Password"), type="password", placeholder="••••••••")
                submitted = st.form_submit_button(t("Sign In"), type="primary", use_container_width=True)
                if submitted:
                    if not email or not password:
                        st.error(t("Please fill in all fields."))
                    else:
                        with st.spinner(t("Signing in...")):
                            try:
                                resp = auth.login(email, password)
                                st.session_state.user = resp.user
                                st.session_state.access_token = resp.session.access_token
                                st.session_state.page = "home"
                                st.success(t("Welcome back! ✨"))
                                st.rerun()
                            except Exception as e:
                                st.error(f"{t('Sign in failed')}: {e}")

        with tab_register:
            with st.form("register_form"):
                st.markdown(f"#### {t('Start your journey')}")
                email = st.text_input(t("Email"), placeholder="you@example.com", key="reg_email")
                password = st.text_input(t("Password"), type="password", placeholder=t("Min 6 characters"), key="reg_pass")
                confirm = st.text_input(t("Confirm password"), type="password", placeholder="••••••••", key="reg_confirm")
                submitted = st.form_submit_button(t("Create Account"), type="primary", use_container_width=True)
                if submitted:
                    if not email or not password or not confirm:
                        st.error(t("Please fill in all fields."))
                    elif password != confirm:
                        st.error(t("Passwords don't match."))
                    elif len(password) < 6:
                        st.error(t("Password must be at least 6 characters."))
                    else:
                        with st.spinner(t("Creating your account...")):
                            try:
                                auth.register(email, password)
                                st.success(t("Account created! Check your email to confirm, then sign in."))
                            except Exception as e:
                                st.error(f"{t('Registration failed')}: {e}")


# ── Sidebar ───────────────────────────────────────────────────────────────────
def show_sidebar():
    with st.sidebar:
        st.markdown("## 🪞 MindMirror")
        user = current_user()
        st.markdown(
            f"<span style='font-size:0.85rem;color:#9b84b0;'>✉️ {user.email}</span>",
            unsafe_allow_html=True,
        )

        # Language selector
        st.divider()
        prev_lang = st.session_state.get("language", "English")
        lang = st.selectbox(
            "🌐 Language",
            LANGUAGES,
            index=LANGUAGES.index(prev_lang),
            key="language",
        )
        if lang != prev_lang:
            st.session_state.language = lang
            st.rerun()

        st.divider()

        pages = {
            t("🏠 Home"): "home",
            t("✍️ New Entry"): "new_entry",
            t("📖 My Journal"): "journal",
            t("📊 Insights"): "analytics",
        }
        for label, page_key in pages.items():
            if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.page = page_key
                st.session_state.pop("viewing_entry", None)
                st.session_state.pop("editing_entry", None)
                st.rerun()

        st.divider()
        if st.button(t("🚪 Sign Out"), use_container_width=True):
            try:
                auth.logout(current_token())
            except Exception:
                pass
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ── Home page ────────────────────────────────────────────────────────────────
def show_home():
    user = current_user()
    hour = datetime.now().hour
    greeting = t("Good morning") if hour < 12 else t("Good afternoon") if hour < 17 else t("Good evening")

    st.markdown(f'<div class="page-title">{greeting} 🌸</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{t("What\'s on your mind today?")}</div>', unsafe_allow_html=True)

    if st.button(t("✍️ Write Today's Entry"), type="primary"):
        st.session_state.page = "new_entry"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    entries = diary.get_entries(current_token(), user.id)
    if not entries:
        st.markdown(f"""
        <div class="mirror-card" style="text-align:center;padding:3rem;">
            <div style="font-size:3rem;">📖</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.3rem;color:#4a3060;margin:0.8rem 0 0.4rem;">{t("Your journal is empty")}</div>
            <div style="color:#9b84b0;font-size:0.9rem;">{t("Write your first entry and let AI help you reflect.")}</div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"#### {t('📝 Recent Entries')}")
    for entry in entries[:3]:
        _render_entry_card(entry, compact=True)

    if len(entries) > 3:
        if st.button(t(f"View all {len(entries)} entries →")):
            st.session_state.page = "journal"
            st.rerun()


# ── New Entry page ────────────────────────────────────────────────────────────
def show_new_entry():
    editing = st.session_state.get("editing_entry")
    title_label = t("Edit Entry") if editing else t("New Entry")

    st.markdown(f'<div class="page-title">✍️ {title_label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{t("Write freely. AI will help you reflect.")}</div>', unsafe_allow_html=True)

    defaults = editing or {}

    with st.form("entry_form", clear_on_submit=False):
        title = st.text_input(t("Title"), value=defaults.get("title", ""), placeholder=t("Give today a title..."))
        mood = st.selectbox(
            t("How are you feeling?"),
            MOODS,
            index=MOODS.index(defaults.get("mood", MOODS[0])) if defaults.get("mood") in MOODS else 0,
        )
        content = st.text_area(
            t("Your entry"),
            value=defaults.get("content", ""),
            placeholder=t("Start writing... let your thoughts flow."),
            height=280,
        )

        col1, col2 = st.columns(2)
        with col1:
            ai_on = st.checkbox(t("✨ Generate AI insights"), value=True)
        with col2:
            submitted = st.form_submit_button(
                t("💾 Save Entry") if editing else t("✨ Save & Reflect"),
                type="primary",
                use_container_width=True,
            )

        if submitted:
            if not title.strip() or not content.strip():
                st.error(t("Please add a title and some content."))
            else:
                user = current_user()
                insights = {}
                if ai_on:
                    with st.spinner(t("🤖 Groq is reading your entry...")):
                        try:
                            insights = ai.generate_all_insights(title, content, mood)
                        except Exception as e:
                            st.warning(f"{t('AI insights unavailable')}: {e}")

                try:
                    if editing:
                        updates = {"title": title, "content": content, "mood": mood, **insights}
                        diary.update_entry(current_token(), editing["id"], user.id, updates)
                        st.success(t("Entry updated! ✨"))
                        st.session_state.pop("editing_entry", None)
                    else:
                        diary.create_entry(
                            current_token(), user.id, title, content, mood,
                            ai_summary=insights.get("ai_summary"),
                            reflection_prompt=insights.get("reflection_prompt"),
                            themes=insights.get("themes", []),
                        )
                        st.success(t("Entry saved! 🌸"))

                    st.session_state.page = "journal"
                    st.rerun()
                except Exception as e:
                    st.error(f"{t('Failed to save entry')}: {e}")

    if mood:
        color = MOOD_COLORS.get(mood, "#C9B1D9")
        st.markdown(f"""
        <div style="margin-top:1rem;display:flex;align-items:center;gap:0.6rem;">
            <div style="width:14px;height:14px;border-radius:50%;background:{color};box-shadow:0 0 8px {color};"></div>
            <span style="font-size:0.85rem;color:#9b84b0;">{t("Currently feeling")} {mood}</span>
        </div>
        """, unsafe_allow_html=True)


# ── Journal page ─────────────────────────────────────────────────────────────
def show_journal():
    viewing = st.session_state.get("viewing_entry")
    if viewing:
        _show_entry_detail(viewing)
        return

    st.markdown(f'<div class="page-title">📖 {t("My Journal")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{t("All your reflections, in one place.")}</div>', unsafe_allow_html=True)

    user = current_user()
    entries = diary.get_entries(current_token(), user.id)

    if not entries:
        st.info(t("No entries yet. Write your first one! ✨"))
        return

    mood_filter = st.selectbox(t("Filter by mood"), [t("All moods")] + MOODS, key="mood_filter")
    if mood_filter != t("All moods") and mood_filter != "All moods":
        entries = [e for e in entries if e.get("mood") == mood_filter]

    st.markdown(
        f"<div style='color:#9b84b0;font-size:0.85rem;margin-bottom:1rem;'>{len(entries)} {t('entries')}</div>",
        unsafe_allow_html=True,
    )

    for entry in entries:
        _render_entry_card(entry, compact=False)


def _render_entry_card(entry: dict, compact: bool = False):
    date_str = datetime.fromisoformat(entry["created_at"]).strftime("%B %d, %Y")
    preview = entry["content"][:180] + "..." if len(entry["content"]) > 180 else entry["content"]
    mood = entry.get("mood", "")

    st.markdown(f"""
    <div class="mirror-card">
        {mood_pill(mood)}
        <div class="entry-title">{entry['title']}</div>
        <div class="entry-meta">📅 {date_str}</div>
        <div class="entry-preview">{preview}</div>
    </div>
    """, unsafe_allow_html=True)

    if not compact:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button(t("📖 Read"), key=f"view_{entry['id']}", use_container_width=True):
                st.session_state.viewing_entry = entry
                st.rerun()
        with col2:
            if st.button(t("✏️ Edit"), key=f"edit_{entry['id']}", use_container_width=True):
                st.session_state.editing_entry = entry
                st.session_state.page = "new_entry"
                st.rerun()
        with col3:
            if st.button(t("🗑️ Delete"), key=f"del_{entry['id']}", use_container_width=True):
                st.session_state[f"confirm_delete_{entry['id']}"] = True

        if st.session_state.get(f"confirm_delete_{entry['id']}"):
            st.warning(t("Are you sure you want to delete this entry?"))
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button(t("Yes, delete"), key=f"yes_{entry['id']}", type="primary"):
                    diary.delete_entry(current_token(), entry["id"], current_user().id)
                    st.session_state.pop(f"confirm_delete_{entry['id']}", None)
                    st.success(t("Entry deleted."))
                    st.rerun()
            with cc2:
                if st.button(t("Cancel"), key=f"no_{entry['id']}"):
                    st.session_state.pop(f"confirm_delete_{entry['id']}", None)
                    st.rerun()
    else:
        if st.button(t("Read →"), key=f"home_view_{entry['id']}"):
            st.session_state.viewing_entry = entry
            st.session_state.page = "journal"
            st.rerun()


def _show_entry_detail(entry: dict):
    if st.button(t("← Back to Journal")):
        st.session_state.pop("viewing_entry", None)
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    date_str = datetime.fromisoformat(entry["created_at"]).strftime("%B %d, %Y · %I:%M %p")
    mood = entry.get("mood", "")

    st.markdown(f"""
    <div class="mirror-card">
        {mood_pill(mood)}
        <div class="page-title">{entry['title']}</div>
        <div class="entry-meta">📅 {date_str}</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.05rem;color:#3d2b52;line-height:1.9;white-space:pre-wrap;margin-top:1rem;">
            {entry['content']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    themes = entry.get("themes") or []
    if themes:
        tags = "".join(f'<span class="theme-tag">#{t}</span>' for t in themes)
        st.markdown(f"<div style='margin-bottom:0.5rem;'>{tags}</div>", unsafe_allow_html=True)

    if entry.get("ai_summary"):
        st.markdown(f"""
        <div class="insight-box">
            <strong>✨ {t('AI Summary')}</strong><br><br>
            {entry['ai_summary']}
        </div>
        """, unsafe_allow_html=True)

    if entry.get("reflection_prompt"):
        st.markdown(f"""
        <div class="reflection-box">
            <strong>💭 {t('Reflection Prompt')}</strong><br><br>
            {entry['reflection_prompt']}
        </div>
        """, unsafe_allow_html=True)


# ── Analytics page ────────────────────────────────────────────────────────────
def show_analytics():
    st.markdown(f'<div class="page-title">📊 {t("Insights")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{t("Patterns in your emotional landscape.")}</div>', unsafe_allow_html=True)

    user = current_user()
    entries = diary.get_entries(current_token(), user.id)
    df = analytics.build_dataframe(entries)
    stats = analytics.get_stats(df)

    col1, col2, col3, col4 = st.columns(4)
    for col, (num, label) in zip(
        [col1, col2, col3, col4],
        [
            (stats["total"], t("Total Entries")),
            (f"{stats['streak']}d", t("Current Streak")),
            (stats["top_mood"], t("Top Mood")),
            (f"{stats['avg_words']}w", t("Avg Words")),
        ],
    ):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{num}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if df.empty or len(df) < 1:
        st.info(t("Write a few entries to unlock your mood analytics! 🌱"))
        return

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**{t('Mood Distribution')}**")
        fig = analytics.mood_distribution_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown(f"**{t('Words Written per Day')}**")
        fig2 = analytics.word_count_chart(df)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)

    if len(df) >= 2:
        st.markdown(f"**{t('Mood over Time')}**")
        fig3 = analytics.mood_timeline_chart(df)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)


# ── Router ────────────────────────────────────────────────────────────────────
def main():
    if not is_logged_in():
        show_auth()
        return

    if "page" not in st.session_state:
        st.session_state.page = "home"

    show_sidebar()

    page = st.session_state.get("page", "home")
    if page == "home":
        show_home()
    elif page == "new_entry":
        show_new_entry()
    elif page == "journal":
        show_journal()
    elif page == "analytics":
        show_analytics()


if __name__ == "__main__":
    main()
