import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import config

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="U-space C2 Readiness Validator",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(config.CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if 'lang' not in st.session_state:
    st.session_state.lang = "Українська"

if 'has_run' not in st.session_state:
    st.session_state.has_run = False

# -----------------------------------------------------------------------------
# LANGUAGE SELECTOR
# -----------------------------------------------------------------------------
selected_lang_name = st.sidebar.selectbox(
    "🌐 Мова / Language",
    options=["Українська", "English"],
    index=["Українська", "English"].index(st.session_state.lang)
)
st.session_state.lang = selected_lang_name

t = config.TRANSLATIONS.get(st.session_state.lang, config.TRANSLATIONS["Українська"])
lang_code = "ua" if st.session_state.lang == "Українська" else "en"

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown(f'<p class="main-header">{t["main_header"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">{t["sub_header"]}</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR: INPUT PARAMETERS, PRESETS & FILE UPLOAD
# -----------------------------------------------------------------------------
st.sidebar.header(t["sidebar_header"])
uploaded_file = st.sidebar.file_uploader(t["file_upload"], type=["csv"])
st.sidebar.markdown("---")

# 1. Network Preset Selector
network_preset_options = [t["preset_none"]] + list(config.NETWORK_PRESETS.keys())
selected_network_preset = st.sidebar.selectbox(
    t["network_preset"],
    options=network_preset_options,
    index=0
)

if selected_network_preset != t["preset_none"]:
    preset_details = config.NETWORK_PRESETS[selected_network_preset]
    st.sidebar.caption(f"💡 {preset_details['help'][lang_code]}")

# 2. Operation Scenario Preset Selector
scenario_preset_options = [t["preset_none"]] + list(config.SCENARIO_PRESETS.keys())
selected_scenario_preset = st.sidebar.selectbox(
    t["scenario_preset"],
    options=scenario_preset_options,
    index=0
)

if selected_scenario_preset != t["preset_none"]:
    preset_details = config.SCENARIO_PRESETS[selected_scenario_preset]
    st.sidebar.caption(f"💡 {preset_details['help'][lang_code]}")

# 3. GNSS Mode Selector
gnss_mode = st.sidebar.selectbox(
    t["gnss_mode"],
    options=["GNSS RTK (0.8 - 2.0 м)", "GNSS 3D Fix (3.0 - 6.0 м)"]
)

st.sidebar.markdown("---")

# ПРІОРИТЕТНОСТЕЙ: Операційний сценарій (SORA) ВИЗНАЧАЄ поріг безпеки L_threshold та f_up
corridor_width = 20.0
l_threshold_ms = 1000
f_up = 2.5
sail_level = "SAIL II"

if selected_scenario_preset != t["preset_none"]:
    sc_params = config.SCENARIO_PRESETS[selected_scenario_preset]["params"]
    corridor_width = sc_params["corridor_width"]
    l_threshold_ms = sc_params["l_threshold"]
    f_up = sc_params["f_up"]
    sail_level = sc_params["sail"]
elif selected_network_preset != t["preset_none"]:
    net_params = config.NETWORK_PRESETS[selected_network_preset]["params"]
    l_threshold_ms = net_params["l_threshold"]
    f_up = net_params["f_up"]
else:
    sail_level = st.sidebar.selectbox(t["sail_class"], ["SAIL II", "SAIL IV"])
    l_threshold_ms = st.sidebar.number_input(t["latency_threshold"], 100, 2000, 1000, 50)

# Run Button
run_btn = st.sidebar.button(
    "▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ / CALCULATE & SIMULATE",
    type="primary",
    use_container_width=True
)

if run_btn:
    st.session_state['has_run'] = True

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data(file_path_or_buffer):
    df = pd.read_csv(file_path_or_buffer)
    if not all(col in df.columns for col in config.REQUIRED_COLUMNS):
        st.error(f"{t['load_error']} {config.REQUIRED_COLUMNS}")
        st.stop()
    return df

if uploaded_file:
    df = load_data(uploaded_file)
    st.sidebar.success(t["log_loaded"])
else:
    st.sidebar.info(t["demo_log"])
    try:
        df = load_data("ideal_flight.csv")
    except Exception:
        try:
            df = load_data("flight_telemetry_log.csv")
        except Exception:
            st.error("Будь ласка, завантажте CSV-файл телеметрії.")
            st.stop()

# -----------------------------------------------------------------------------
# EXECUTION GUARD: STRICTLY BY BUTTON CLICK
# -----------------------------------------------------------------------------
if not st.session_state.get('has_run', False):
    st.info("👈 Налаштуйте вхідні параметри або оберіть пресети у бічній панелі та натисніть кнопку [▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ], щоб розпочати діагностику.")
    st.stop()

# -----------------------------------------------------------------------------
# MAIN LOGIC & COMPUTATIONS (Executed strictly after clicking the button)
# -----------------------------------------------------------------------------

# 1. Clock Drift Correction & Latency Metrics
raw_latencies = df['timestamp_server_ms'] - df['timestamp_board_ms']
clock_offset = np.min(raw_latencies)
latencies = np.maximum(raw_latencies - clock_offset, 1.0)
l_p95 = np.percentile(latencies, 95)
mean_latency = np.mean(latencies)

# 2. Latency Factor (f_L)
f_L = max(0.0, min(1.0, (config.L_MAX - l_p95) / (config.L_MAX - l_threshold_ms)))

# 3. C2 Availability
expected_packets_avail = (df['timestamp_board_ms'].iloc[-1] - df['timestamp_board_ms'].iloc[0]) / (1000 / f_up)
availability = max(0.0, min(1.0, len(df) / expected_packets_avail))

# 4. Temporal Continuity
t_gaps = np.diff(df['timestamp_board_ms']) / 1000.0
outage_time = np.sum(t_gaps[t_gaps > 2.0])
total_time = (df['timestamp_board_ms'].iloc[-1] - df['timestamp_board_ms'].iloc[0]) / 1000.0
continuity = max(0.0, min(1.0, 1.0 - (outage_time / total_time))) if total_time > 0 else 1.0

# 5. Combined C2 Integrity (I_data * I_gnss)
expected_packets_int = df['seq_id'].max() - df['seq_id'].min() + 1
i_data = max(0.0, min(1.0, len(df) / expected_packets_int)) if expected_packets_int > 0 else 1.0

if 'gnss_fix_type' in df.columns:
    if gnss_mode == "GNSS RTK (0.8 - 2.0 м)":
        i_gnss = float((df['gnss_fix_type'] == 4).mean())
    else:
        i_gnss = float((df['gnss_fix_type'] >= 3).mean())
    c2_integrity = i_data * i_gnss
else:
    c2_integrity = i_data

# 6. Weights according to SAIL level
if sail_level == "SAIL II":
    w_A, w_C, w_L, w_I = config.WEIGHTS_SAIL_II
else:
    w_A, w_C, w_L, w_I = config.WEIGHTS_SAIL_IV

# 7. Final R_C2 Calculation
R_C2 = w_A * availability + w_C * continuity + w_L * f_L + w_I * c2_integrity
R_C2_pct = R_C2 * 100.0

# -----------------------------------------------------------------------------
# MAIN DASHBOARD LAYOUT
# -----------------------------------------------------------------------------
col_status, col_verdict = st.columns([1, 2])
with col_status:
    st.markdown(f"### {t['integral_indicator']}")
    st.metric(label=t["readiness_level"], value=f"{R_C2_pct:.1f}%", delta=f"{R_C2_pct - config.R_C2_THRESHOLD_PCT:.1f}% {t['threshold_text']}")
with col_verdict:
    st.markdown(f"### {t['verdict_header']}")
    if R_C2_pct >= config.R_C2_THRESHOLD_PCT:
        st.markdown(f'<div class="status-approved">{t["approved"].format(corridor_width)}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-rejected">{t["rejected"]}</div>', unsafe_allow_html=True)

st.markdown("---")

# Key Indicators KPI Row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(t["availability"], f"{availability*100:.2f}%", t["availability_target"])
kpi2.metric(t["continuity"], f"{continuity*100:.2f}%", t["continuity_target"])
kpi3.metric(t["integrity"], f"{c2_integrity*100:.2f}%", t["integrity_target"])
kpi4.metric(t["latency"], f"{l_p95:.1f} ms", f"Mean: {mean_latency:.1f} ms")

st.markdown("---")

# -----------------------------------------------------------------------------
# CHARTS & DIAGNOSTICS SECTION
# -----------------------------------------------------------------------------
tab_summary, tab_sensitivity, tab_monte_carlo, tab_telemetry = st.tabs([
    t["tab_analysis"], t["tab_sensitivity"], t["tab_monte_carlo"], t["tab_telemetry"]
])

with tab_summary:
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader(t["latency_distribution"])
        fig_lat = px.histogram(x=latencies, nbins=50, labels={'x': t["latency_xlabel"], 'y': t["latency_ylabel"]})
        fig_lat.add_vline(x=l_threshold_ms, line_dash="dash", line_color="red", annotation_text=t["threshold_annotation"].format(l_threshold_ms))
        st.plotly_chart(fig_lat, use_container_width=True)

    with col_chart2:
        st.subheader(t["radar_title"])
        categories = t["radar_categories"]
        values = [availability * 100, continuity * 100, f_L * 100, c2_integrity * 100]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', name=t["current_board"]))
        fig_radar.add_trace(go.Scatterpolar(r=[80, 80, 80, 80, 80], theta=categories + [categories[0]], name=t["min_threshold"], line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
        st.plotly_chart(fig_radar, use_container_width=True)

with tab_sensitivity:
    st.subheader("🔬 Sensitivity Analysis (Аналіз чутливості вагових коефіцієнтів)")
    delta = config.SENSITIVITY_DELTA
    sensitivity_results = {
        "Availability (+10%)": (w_A + delta) * availability + w_C * continuity + w_L * f_L + w_I * c2_integrity,
        "Continuity (+10%)": w_A * availability + (w_C + delta) * continuity + w_L * f_L + w_I * c2_integrity,
        "Latency Factor (+10%)": w_A * availability + w_C * continuity + (w_L + delta) * f_L + w_I * c2_integrity,
        "Integrity (+10%)": w_A * availability + w_C * continuity + w_L * f_L + (w_I + delta) * c2_integrity,
    }
    df_sens = pd.DataFrame([
        {"Factor": k, "R_C2 (%)": v * 100.0, "Delta (%)": (v - R_C2) * 100.0}
        for k, v in sensitivity_results.items()
    ])
    fig_sens = px.bar(df_sens, x="Factor", y="R_C2 (%)", text_auto='.1f', color="Delta (%)", color_continuous_scale="Viridis")
    fig_sens.add_hline(y=config.R_C2_THRESHOLD_PCT, line_dash="dash", line_color="red")
    st.plotly_chart(fig_sens, use_container_width=True)

with tab_monte_carlo:
    st.subheader(t["monte_carlo_title"])
    n_simulations = 1000
    mu = np.log(max(mean_latency, 1.0)) - 0.5 * (0.4 ** 2)
    simulated_latencies = np.random.lognormal(mean=mu, sigma=0.4, size=n_simulations)
    
    sim_f_L = np.array([max(0.0, min(1.0, (config.L_MAX - sl) / (config.L_MAX - l_threshold_ms))) for sl in simulated_latencies])

    sim_availability = np.random.beta(a=max(availability * 100, 1), b=max((1 - availability) * 100, 1), size=n_simulations)
    sim_continuity = np.random.beta(a=max(continuity * 100, 1), b=max((1 - continuity) * 100, 1), size=n_simulations)
    sim_integrity = np.random.beta(a=max(c2_integrity * 100, 1), b=max((1 - c2_integrity) * 100, 1), size=n_simulations)

    sim_R_C2 = w_A * sim_availability + w_C * sim_continuity + w_L * sim_f_L + w_I * sim_integrity
    sim_R_C2_pct = sim_R_C2 * 100.0

    fig_mc = px.histogram(x=sim_R_C2_pct, nbins=50, labels={'x': t["monte_carlo_xlabel"], 'y': t["monte_carlo_ylabel"]})
    fig_mc.add_vline(x=config.R_C2_THRESHOLD_PCT, line_dash="dash", line_color="red", annotation_text="80% Threshold")
    st.plotly_chart(fig_mc, use_container_width=True)
    
    prob_success = np.mean(sim_R_C2_pct >= config.R_C2_THRESHOLD_PCT) * 100.0
    st.metric(label=t["probability_text"].split("=")[0], value=f"{prob_success:.1f}%", delta=f"Mean R_C2: {np.mean(sim_R_C2_pct):.1f}%")

with tab_telemetry:
    if 'lat' in df.columns and 'lon' in df.columns:
        st.subheader(t["flight_map"])
        st.map(df[['lat', 'lon']])
    st.subheader(t["raw_log"])
    st.dataframe(df.head(20))

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(t["footer"])