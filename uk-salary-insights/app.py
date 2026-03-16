import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="UK Salary Insights", page_icon="💸", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0a0e1a; }
    .block-container { padding: 2rem 3rem; }
    h1 {
        background: linear-gradient(90deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 900 !important;
    }
    h2, h3 { color: #ffffff; }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #FFD700 !important;
    }
    div[data-testid="stMetricLabel"] { color: #aaa !important; }
    .stTabs [data-baseweb="tab"] {
        color: #aaa;
        font-size: 1rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] { color: #FFD700 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💸 UK Salary Insights 2024</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#aaa; font-size:1.1rem'>Explore salaries across jobs, cities and industries in the UK</p>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_data():
    jobs = [
        "Data Analyst","Data Analyst","Data Analyst","Data Analyst","Data Analyst",
        "Data Scientist","Data Scientist","Data Scientist","Data Scientist","Data Scientist",
        "Software Engineer","Software Engineer","Software Engineer","Software Engineer","Software Engineer",
        "BI Analyst","BI Analyst","BI Analyst","BI Analyst","BI Analyst",
        "Machine Learning Engineer","Machine Learning Engineer","Machine Learning Engineer","Machine Learning Engineer",
        "Product Manager","Product Manager","Product Manager","Product Manager",
        "DevOps Engineer","DevOps Engineer","DevOps Engineer","DevOps Engineer",
        "Cybersecurity Analyst","Cybersecurity Analyst","Cybersecurity Analyst","Cybersecurity Analyst",
        "Cloud Architect","Cloud Architect","Cloud Architect","Cloud Architect",
        "UX Designer","UX Designer","UX Designer","UX Designer",
        "Finance Analyst","Finance Analyst","Finance Analyst","Finance Analyst",
        "Marketing Analyst","Marketing Analyst","Marketing Analyst","Marketing Analyst",
        "HR Analyst","HR Analyst","HR Analyst","HR Analyst",
        "Operations Analyst","Operations Analyst","Operations Analyst","Operations Analyst",
        "Business Analyst","Business Analyst","Business Analyst","Business Analyst",
        "Reporting Analyst","Reporting Analyst","Reporting Analyst","Reporting Analyst",
        "AI Engineer","AI Engineer","AI Engineer","AI Engineer",
        "Database Administrator","Database Administrator","Database Administrator",
        "Statistician","Statistician","Statistician",
        "Quantitative Analyst","Quantitative Analyst","Quantitative Analyst",
    ]
    cities = [
        "London","Manchester","Birmingham","Edinburgh","Bristol",
        "London","Manchester","Birmingham","Edinburgh","Bristol",
        "London","Manchester","Birmingham","Edinburgh","Bristol",
        "London","Manchester","Birmingham","Edinburgh","Bristol",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham","Edinburgh",
        "London","Manchester","Birmingham",
        "London","Manchester","Birmingham",
        "London","Manchester","Birmingham",
    ]
    industries = [
        "Technology","Technology","Technology","Technology","Technology",
        "Technology","Technology","Technology","Technology","Technology",
        "Technology","Technology","Technology","Technology","Technology",
        "Technology","Technology","Technology","Technology","Technology",
        "Technology","Technology","Technology","Technology",
        "Technology","Technology","Technology","Technology",
        "Technology","Technology","Technology","Technology",
        "Security","Security","Security","Security",
        "Technology","Technology","Technology","Technology",
        "Design","Design","Design","Design",
        "Finance","Finance","Finance","Finance",
        "Marketing","Marketing","Marketing","Marketing",
        "HR","HR","HR","HR",
        "Operations","Operations","Operations","Operations",
        "Consulting","Consulting","Consulting","Consulting",
        "Analytics","Analytics","Analytics","Analytics",
        "Technology","Technology","Technology","Technology",
        "Technology","Technology","Technology",
        "Research","Research","Research",
        "Finance","Finance","Finance",
    ]
    experience = [
        "Mid","Mid","Junior","Mid","Junior",
        "Senior","Senior","Mid","Senior","Mid",
        "Senior","Senior","Mid","Senior","Mid",
        "Mid","Mid","Junior","Mid","Junior",
        "Senior","Senior","Mid","Senior",
        "Senior","Senior","Mid","Senior",
        "Senior","Mid","Mid","Senior",
        "Mid","Mid","Junior","Mid",
        "Senior","Senior","Senior","Mid",
        "Mid","Junior","Junior","Mid",
        "Senior","Mid","Mid","Senior",
        "Mid","Junior","Junior","Mid",
        "Junior","Junior","Entry","Junior",
        "Mid","Junior","Junior","Mid",
        "Mid","Mid","Junior","Mid",
        "Junior","Junior","Entry","Junior",
        "Senior","Senior","Mid","Senior",
        "Mid","Mid","Junior",
        "Mid","Mid","Junior",
        "Senior","Senior","Mid",
    ]
    salaries = [
        55000,42000,38000,48000,40000,
        85000,65000,58000,72000,62000,
        90000,70000,62000,75000,65000,
        52000,40000,36000,45000,38000,
        95000,75000,68000,80000,
        88000,72000,65000,78000,
        82000,65000,60000,72000,
        65000,50000,45000,55000,
        105000,85000,78000,88000,
        58000,42000,38000,48000,
        75000,58000,52000,68000,
        48000,35000,32000,42000,
        38000,30000,28000,35000,
        52000,38000,35000,45000,
        62000,52000,45000,58000,
        40000,32000,28000,36000,
        98000,78000,72000,85000,
        58000,45000,40000,
        62000,50000,45000,
        95000,80000,72000,
    ]
    return pd.DataFrame({
        "job_title": jobs,
        "city": cities,
        "industry": industries,
        "experience": experience,
        "salary": salaries
    })

df = load_data()

# ── METRICS ──
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Highest Salary", f"£{df['salary'].max():,}")
col2.metric("📊 Average UK Salary", f"£{int(df['salary'].mean()):,}")
col3.metric("🏙️ Cities Covered", df['city'].nunique())
col4.metric("💼 Job Titles", df['job_title'].nunique())
st.markdown("---")

# ── FILTERS ──
st.markdown("### 🔍 Filter Salaries")
col1, col2, col3 = st.columns(3)
with col1:
    selected_city = st.multiselect("🏙️ Select Cities",
                                    sorted(df['city'].unique()),
                                    default=sorted(df['city'].unique()))
with col2:
    selected_industry = st.multiselect("🏭 Select Industry",
                                        sorted(df['industry'].unique()),
                                        default=sorted(df['industry'].unique()))
with col3:
    selected_exp = st.multiselect("⭐ Experience Level",
                                   ["Entry","Junior","Mid","Senior"],
                                   default=["Entry","Junior","Mid","Senior"])

if selected_city and selected_industry and selected_exp:
    df_filtered = df[
        (df['city'].isin(selected_city)) &
        (df['industry'].isin(selected_industry)) &
        (df['experience'].isin(selected_exp))
    ]
else:
    df_filtered = df.copy()

if df_filtered.empty:
    st.warning("No data found. Showing all data.")
    df_filtered = df.copy()

st.markdown(f"**Showing {len(df_filtered)} salary records**")
st.markdown("---")

PLOT_BG = "#0a0e1a"
PAPER_BG = "#0a0e1a"

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️  Salary Map",
    "💼  By Job Title",
    "🏙️  By City",
    "📈  Experience",
    "🏭  By Industry"
])

# ── TAB 1: MAP ──
with tab1:
    st.markdown("### 🗺️ Average Salary by UK City")
    city_coords = {
        "London": (51.5074, -0.1278),
        "Manchester": (53.4808, -2.2426),
        "Birmingham": (52.4862, -1.8904),
        "Edinburgh": (55.9533, -3.1883),
        "Bristol": (51.4545, -2.5879),
    }
    city_avg = df_filtered.groupby("city")["salary"].mean().reset_index()
    city_avg.columns = ["city", "avg_salary"]
    city_avg["lat"] = city_avg["city"].map(lambda x: city_coords.get(x,(51.5,-1.0))[0])
    city_avg["lon"] = city_avg["city"].map(lambda x: city_coords.get(x,(51.5,-1.0))[1])
    city_avg["salary_fmt"] = city_avg["avg_salary"].apply(lambda x: f"£{int(x):,}")

    fig_map = px.scatter_mapbox(
        city_avg, lat="lat", lon="lon",
        size="avg_salary", color="avg_salary",
        hover_name="city",
        hover_data={"salary_fmt":True,"avg_salary":False,"lat":False,"lon":False},
        color_continuous_scale="Oranges",
        size_max=60, zoom=5,
        mapbox_style="carto-darkmatter",
        title="💰 Average Salary by City"
    )
    fig_map.update_layout(height=500, paper_bgcolor=PAPER_BG, font=dict(color="white"))
    st.plotly_chart(fig_map, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_city_bar = px.bar(
            city_avg.sort_values("avg_salary", ascending=False),
            x="city", y="avg_salary",
            color="avg_salary", color_continuous_scale="Oranges",
            title="📊 Average Salary by City",
            template="plotly_dark", text="salary_fmt"
        )
        fig_city_bar.update_traces(textposition="outside")
        fig_city_bar.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                                   font=dict(color="white"))
        st.plotly_chart(fig_city_bar, use_container_width=True)

    with col2:
        fig_box = px.box(
            df_filtered, x="city", y="salary", color="city",
            title="📦 Salary Distribution by City",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_box.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                              font=dict(color="white"), showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

# ── TAB 2: JOB TITLE ──
with tab2:
    st.markdown("### 💼 Salaries by Job Title")
    job_avg = df_filtered.groupby("job_title")["salary"].mean().reset_index()
    job_avg.columns = ["job_title","avg_salary"]
    job_avg = job_avg.sort_values("avg_salary", ascending=True)
    job_avg["salary_fmt"] = job_avg["avg_salary"].apply(lambda x: f"£{int(x):,}")

    fig_job = px.bar(
        job_avg, x="avg_salary", y="job_title",
        orientation="h",
        color="avg_salary", color_continuous_scale="Oranges",
        title="💼 Average Salary by Job Title",
        template="plotly_dark", text="salary_fmt"
    )
    fig_job.update_traces(textposition="outside")
    fig_job.update_layout(
        height=600, paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color="white"), yaxis=dict(tickfont=dict(size=11))
    )
    st.plotly_chart(fig_job, use_container_width=True)

    st.markdown("### 🔍 Search Specific Job Title")
    job_options = sorted(df_filtered["job_title"].unique().tolist())
    if job_options:
        search = st.selectbox("Select a job title to explore", job_options)
        job_data = df_filtered[df_filtered['job_title'] == search]
        if not job_data.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("💰 Average Salary", f"£{int(job_data['salary'].mean()):,}")
            c2.metric("📈 Highest Salary", f"£{int(job_data['salary'].max()):,}")
            c3.metric("📉 Lowest Salary", f"£{int(job_data['salary'].min()):,}")

            col1, col2 = st.columns(2)
            with col1:
                fig_search = px.bar(
                    job_data.sort_values("salary", ascending=False),
                    x="city", y="salary", color="experience",
                    title=f"💼 {search} — Salary by City",
                    template="plotly_dark", barmode="group",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig_search.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                                         font=dict(color="white"))
                st.plotly_chart(fig_search, use_container_width=True)

            with col2:
                exp_job_data = job_data.groupby("experience")["salary"].mean().reset_index()
                fig_exp_job = px.bar(
                    exp_job_data, x="experience", y="salary",
                    color="salary", color_continuous_scale="Oranges",
                    title=f"📈 {search} — Salary by Experience",
                    template="plotly_dark",
                    category_orders={"experience":["Entry","Junior","Mid","Senior"]}
                )
                fig_exp_job.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                                          font=dict(color="white"))
                st.plotly_chart(fig_exp_job, use_container_width=True)

# ── TAB 3: CITY ──
with tab3:
    st.markdown("### 🏙️ City Salary Comparison")

    pivot = df_filtered.pivot_table(
        index="job_title", columns="city", values="salary", aggfunc="mean"
    )
    fig_heatmap = px.imshow(
        pivot,
        title="🌡️ Salary Heatmap — Job Title vs City",
        template="plotly_dark",
        color_continuous_scale="Oranges",
        aspect="auto", text_auto=".2s"
    )
    fig_heatmap.update_layout(height=550, paper_bgcolor=PAPER_BG,
                              font=dict(color="white"))
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("### ⚔️ Compare Two Cities")
    city_list = sorted(df_filtered['city'].unique().tolist())
    col1, col2 = st.columns(2)
    with col1:
        city1 = st.selectbox("Select City 1", city_list, index=0)
    with col2:
        city2_opts = [c for c in city_list if c != city1]
        city2 = st.selectbox("Select City 2", city2_opts, index=0)

    df_compare_avg = df_filtered[df_filtered['city'].isin([city1,city2])]\
        .groupby(["job_title","city"])["salary"].mean().reset_index()

    fig_compare = px.bar(
        df_compare_avg, x="job_title", y="salary",
        color="city", barmode="group",
        title=f"⚔️ {city1} vs {city2} — Salary Comparison",
        template="plotly_dark",
        color_discrete_sequence=["#FFD700","#FF6B6B"]
    )
    fig_compare.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        xaxis_tickangle=45, font=dict(color="white"), height=500
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    fig_violin = px.violin(
        df_filtered, x="city", y="salary", color="city", box=True,
        title="🎻 Salary Violin Chart by City",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_violin.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                             font=dict(color="white"), showlegend=False)
    st.plotly_chart(fig_violin, use_container_width=True)

# ── TAB 4: EXPERIENCE ──
with tab4:
    st.markdown("### 📈 Salary by Experience Level")
    exp_order = ["Entry","Junior","Mid","Senior"]

    exp_avg = df_filtered.groupby("experience")["salary"].mean().reset_index()
    exp_avg.columns = ["experience","avg_salary"]
    exp_avg["experience"] = pd.Categorical(exp_avg["experience"],
                                           categories=exp_order, ordered=True)
    exp_avg = exp_avg.sort_values("experience")
    exp_avg["salary_fmt"] = exp_avg["avg_salary"].apply(lambda x: f"£{int(x):,}")

    col1, col2 = st.columns(2)
    with col1:
        fig_exp_line = px.line(
            exp_avg, x="experience", y="avg_salary",
            title="📈 Average Salary by Experience",
            template="plotly_dark", markers=True,
            color_discrete_sequence=["#FFD700"], text="salary_fmt"
        )
        fig_exp_line.update_traces(line=dict(width=3), marker=dict(size=12),
                                   textposition="top center")
        fig_exp_line.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                                   font=dict(color="white"))
        st.plotly_chart(fig_exp_line, use_container_width=True)

    with col2:
        fig_exp_bar = px.bar(
            exp_avg, x="experience", y="avg_salary",
            color="avg_salary", color_continuous_scale="Oranges",
            title="💰 Salary by Experience",
            template="plotly_dark", text="salary_fmt",
            category_orders={"experience": exp_order}
        )
        fig_exp_bar.update_traces(textposition="outside")
        fig_exp_bar.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                                  font=dict(color="white"))
        st.plotly_chart(fig_exp_bar, use_container_width=True)

    st.markdown("### 💡 Experience Level Insights")
    c1, c2, c3, c4 = st.columns(4)
    for col, exp in zip([c1,c2,c3,c4], exp_order):
        exp_data = df_filtered[df_filtered["experience"] == exp]
        if not exp_data.empty:
            col.metric(f"⭐ {exp}", f"£{int(exp_data['salary'].mean()):,}")

    fig_exp_box = px.box(
        df_filtered, x="experience", y="salary", color="experience",
        title="📦 Salary Range by Experience Level",
        template="plotly_dark",
        category_orders={"experience": exp_order},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_exp_box.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                              font=dict(color="white"), showlegend=False)
    st.plotly_chart(fig_exp_box, use_container_width=True)

    exp_city = df_filtered.groupby(["experience","city"])["salary"].mean().reset_index()
    exp_city["experience"] = pd.Categorical(exp_city["experience"],
                                            categories=exp_order, ordered=True)
    exp_city = exp_city.sort_values("experience")

    fig_exp_city = px.line(
        exp_city, x="experience", y="salary", color="city",
        markers=True,
        title="📈 Salary Progression by City & Experience",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Bold,
        category_orders={"experience": exp_order}
    )
    fig_exp_city.update_traces(line=dict(width=2.5), marker=dict(size=10))
    fig_exp_city.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                               font=dict(color="white"))
    st.plotly_chart(fig_exp_city, use_container_width=True)

# ── TAB 5: INDUSTRY ──
with tab5:
    st.markdown("### 🏭 Salary by Industry")

    ind_avg = df_filtered.groupby("industry")["salary"].mean().reset_index()
    ind_avg.columns = ["industry","avg_salary"]
    ind_avg = ind_avg.sort_values("avg_salary", ascending=False)
    ind_avg["salary_fmt"] = ind_avg["avg_salary"].apply(lambda x: f"£{int(x):,}")

    fig_ind = px.bar(
        ind_avg, x="industry", y="avg_salary",
        color="avg_salary", color_continuous_scale="Oranges",
        title="🏭 Average Salary by Industry",
        template="plotly_dark", text="salary_fmt"
    )
    fig_ind.update_traces(textposition="outside")
    fig_ind.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                          font=dict(color="white"))
    st.plotly_chart(fig_ind, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_sunburst = px.sunburst(
            df_filtered, path=["industry","job_title"],
            values="salary",
            title="☀️ Salary by Industry & Job",
            template="plotly_dark",
            color="salary", color_continuous_scale="Oranges"
        )
        fig_sunburst.update_layout(height=500, paper_bgcolor=PAPER_BG,
                                   font=dict(color="white"))
        st.plotly_chart(fig_sunburst, use_container_width=True)

    with col2:
        fig_pie = px.pie(
            ind_avg, names="industry", values="avg_salary",
            title="🥧 Salary Share by Industry",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_pie.update_layout(paper_bgcolor=PAPER_BG, font=dict(color="white"))
        st.plotly_chart(fig_pie, use_container_width=True)

    ind_exp = df_filtered.groupby(["industry","experience"])["salary"].mean().reset_index()
    fig_ind_exp = px.bar(
        ind_exp, x="industry", y="salary",
        color="experience", barmode="group",
        title="🏭 Industry Salary by Experience Level",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Bold,
        category_orders={"experience":["Entry","Junior","Mid","Senior"]}
    )
    fig_ind_exp.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        xaxis_tickangle=45, font=dict(color="white")
    )
    st.plotly_chart(fig_ind_exp, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#555'>UK Salary Insights 2024 | Built by Vinothini | vinothini45.github.io</p>",
            unsafe_allow_html=True)