import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend.config import MOOD_COLORS


def build_dataframe(entries: list) -> pd.DataFrame:
    if not entries:
        return pd.DataFrame()
    df = pd.DataFrame(entries)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["date"] = df["created_at"].dt.date
    df["word_count"] = df["content"].apply(lambda x: len(str(x).split()))
    return df


def mood_distribution_chart(df: pd.DataFrame):
    if df.empty:
        return None
    mood_counts = df["mood"].value_counts().reset_index()
    mood_counts.columns = ["mood", "count"]
    colors = [MOOD_COLORS.get(m, "#A8DADC") for m in mood_counts["mood"]]
    fig = px.pie(
        mood_counts,
        names="mood",
        values="count",
        color_discrete_sequence=colors,
        hole=0.45,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=13),
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(orientation="v", x=1.02, y=0.5),
        showlegend=True,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def mood_timeline_chart(df: pd.DataFrame):
    if df.empty or len(df) < 2:
        return None
    mood_order = list(MOOD_COLORS.keys())
    df = df.copy()
    df["mood_index"] = df["mood"].apply(
        lambda m: mood_order.index(m) if m in mood_order else 0
    )
    df_sorted = df.sort_values("created_at")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sorted["created_at"],
        y=df_sorted["mood"],
        mode="lines+markers",
        marker=dict(
            color=[MOOD_COLORS.get(m, "#A8DADC") for m in df_sorted["mood"]],
            size=12,
            line=dict(width=2, color="white"),
        ),
        line=dict(color="#C9B1D9", width=2, dash="dot"),
        text=df_sorted["title"],
        hovertemplate="<b>%{text}</b><br>%{y}<br>%{x|%b %d, %Y}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12),
        xaxis=dict(showgrid=False, zeroline=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="#EDE8F5", zeroline=False, title=""),
        margin=dict(t=20, b=40, l=10, r=10),
        hovermode="closest",
    )
    return fig


def word_count_chart(df: pd.DataFrame):
    if df.empty:
        return None
    df_sorted = df.sort_values("created_at")
    fig = px.bar(
        df_sorted,
        x="date",
        y="word_count",
        color="mood",
        color_discrete_map=MOOD_COLORS,
        labels={"word_count": "Words Written", "date": ""},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#EDE8F5"),
        margin=dict(t=20, b=40, l=10, r=10),
        legend_title="Mood",
        showlegend=False,
    )
    return fig


def get_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"total": 0, "streak": 0, "top_mood": "—", "avg_words": 0}
    total = len(df)
    avg_words = int(df["word_count"].mean())
    top_mood = df["mood"].value_counts().idxmax()

    # streak calculation
    dates = sorted(df["date"].unique(), reverse=True)
    streak = 0
    from datetime import date, timedelta
    today = date.today()
    for i, d in enumerate(dates):
        expected = today - timedelta(days=i)
        if d == expected:
            streak += 1
        else:
            break

    return {"total": total, "streak": streak, "top_mood": top_mood, "avg_words": avg_words}
