import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="U-space C2 Readiness Validator",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0F2C59;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4F709C;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #0F2C59;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .status-approved {
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.2rem;
        border: 1px solid #A5D6A7;
    }
    .status-rejected {
        background-color: #FFEBEE;
        color: #C62828;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.2rem;
        border: 1px solid #EF9A9A;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">🛸 U-space C2 Readiness Diagnostic Validator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">B2B передпольотна експрес-діагностика та аналіз "вузьких місць" C2-лінку БАС (за вимогами Regulation EU 2021/664)</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR: INPUT PARAMETERS & FILE UPLOAD
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Вхідні параметри та сценарій")

uploaded_file = st.sidebar.file_uploader("📁 Завантажити лог телеметрії (CSV)", type=["csv"])

st.sidebar.subheader("1. Сценарій U-space та Геозона")
corridor_width_m = st.sidebar.slider("Ширина коридору OIV (м)", min_value=10.0, max_value=50.0, value=20.0, step=5.0)
sail_level = st.sidebar.selectbox("Клас ризику SORA 2.5 (SAIL)", options=["SAIL II (Низький міський ризик)", "SAIL IV (Високий міський ризик)"], index=0)
l_threshold_ms = st.sidebar.number_input("Нормативний поріг затримки L_threshold (мс)", min_value=100, max_value=2000, value=1000, step=50)

st.sidebar.subheader("2. Паспортні характеристики БАС")
telemetry_freq_hz = st.sidebar.slider("Частота відправки телеметрії f_up (Гц)", min_value=0.5, max_value=10.0, value=2.5, step=0.5)
gnss_type = st.sidebar.selectbox("Режим супутникової навігації", options=["GNSS RTK (0.8 - 2.0 м)", "GNSS 3D Fix (3.0 - 6.0 м)"], index=0)

# Weights according to SAIL level
if "SAIL II" in sail_level:
    w_A, w_C, w_L, w_I = 0.35, 0.25, 0.25, 0.15
else: # SAIL IV
    w_A, w_C, w_L, w_I = 0.25, 0.30, 0.25, 0.20

# -----------------------------------------------------------------------------
# DATA LOADING & PARSING FUNCTION
# -----------------------------------------------------------------------------
@st.cache_data
def load_data(file_path_or_buffer):
    df = pd.read_csv(file_path_or_buffer)
    # End-to-End Latency
    df['latency_ms'] = df['timestamp_server_ms'] - df['timestamp_board_ms']
    return df

if uploaded_file is not None:
    df_telemetry = load_data(uploaded_file)
    st.sidebar.success("✅ Лог телеметрії успішно завантажено!")
else:
    # Use default mock dataset
    try:
        df_telemetry = load_data('flight_telemetry_log.csv')
        st.sidebar.info("ℹ️ Використовується демо-лог польоту у міському каньйоні.")
    except Exception:
        st.error("Помилка завантаження тестового файлу логу.")
        st.stop()

# -----------------------------------------------------------------------------
# CORE C2 METRICS CALCULATION
# -----------------------------------------------------------------------------
total_packets = len(df_telemetry)
min_seq, max_seq = df_telemetry['seq_id'].min(), df_telemetry['seq_id'].max()
expected_packets = max_seq - min_seq + 1
dropped_packets = expected_packets - total_packets
packet_loss_rate = (dropped_packets / expected_packets) if expected_packets > 0 else 0.0

# Mean Latency
mean_latency = df_telemetry['latency_ms'].mean()
p95_latency = df_telemetry['latency_ms'].quantile(0.95)

# Normalized Latency f_L
L_max = 5000.0 # Upper breakdown threshold 5 seconds
f_L = max(0.0, min(1.0, (L_max - mean_latency) / (L_max - l_threshold_ms)))

# Availability (A) = 1 - Packet Loss
availability = max(0.0, 1.0 - packet_loss_rate)

# Continuity (C): fraction of interval without severe gap (> 2000 ms)
time_diffs_ms = df_telemetry['timestamp_server_ms'].diff().dropna()
outages = (time_diffs_ms > 2000).sum()
continuity = max(0.0, 1.0 - (outages / len(time_diffs_ms))) if len(time_diffs_ms) > 0 else 1.0

# Integrity (I): based on valid GNSS fix and non-corrupted packets
integrity = (df_telemetry['gnss_fix_type'] >= 3).mean()

# Integral Indicator R_C2
R_C2 = w_A * availability + w_C * continuity + w_L * f_L + w_I * integrity
R_C2_pct = R_C2 * 100.0

# -----------------------------------------------------------------------------
# MAIN DASHBOARD LAYOUT
# -----------------------------------------------------------------------------
col_status, col_verdict = st.columns([1, 2])

with col_status:
    st.markdown("### Інтегральний показник $R_{C2}$")
    st.metric(label="Рівень готовності C2-лінку", value=f"{R_C2_pct:.1f}%", delta=f"{R_C2_pct - 80.0:.1f}% від порогу (80%)")

with col_verdict:
    st.markdown("### Вердикт передпольотного тестування")
    if R_C2_pct >= 80.0:
        st.markdown(f'<div class="status-approved">✅ APPROVED — C2-лінк готовий до виконання місії у коридорі {corridor_width_m:.0f} м</div>', unsafe_allow_html=True)
        st.write("БАС відповідає вимогам авторизації U-plan. Імовірність втрати відповідності під час польоту не перевищує припустимі норми.")
    else:
        st.markdown(f'<div class="status-rejected">🚨 REJECTED — ВИЯВЛЕНО ВУЗЬКЕ МІСЦЕ (BOTTLENECK)</div>', unsafe_allow_html=True)
        st.write("C2-лінк у поточній конфігурації має підвищений ризик деградації. Потрібна коригувальна дія до вильоту.")

st.markdown("---")

# Key Indicators KPI Row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Доступність (Availability)", f"{availability*100:.2f}%", "Ціль: >98.0%")
with kpi2:
    st.metric("Безперервність (Continuity)", f"{continuity*100:.2f}%", "Ціль: >99.0%")
with kpi3:
    st.metric("Затримка (Mean Latency)", f"{mean_latency:.1f} мс", f"P95: {p95_latency:.1f} мс")
with kpi4:
    st.metric("Втрата пакетів (Packet Loss)", f"{packet_loss_rate*100:.2f}%", f"Пропущено: {dropped_packets} пк")

st.markdown("---")

# -----------------------------------------------------------------------------
# CHARTS & DIAGNOSTICS SECTION
# -----------------------------------------------------------------------------
tab_summary, tab_sensitivity, tab_telemetry = st.tabs(["📊 Ботлнек-Аналіз та Графіки", "🔬 Аналіз Чутливості (Sensitivity)", "🗺️ Лог та Маршрут Місії"])

with tab_summary:
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Розподіл затримок мережі (End-to-End Latency)")
        fig_lat = px.histogram(
            df_telemetry, 
            x="latency_ms", 
            nbins=40, 
            color_discrete_sequence=['#0F2C59'],
            labels={'latency_ms': 'Затримка (мс)', 'count': 'Кількість пакетів'},
            title="Гістограма затримок у сотовому каналі 4G/5G"
        )
        fig_lat.add_vline(x=l_threshold_ms, line_dash="dash", line_color="red", annotation_text="Поріг U-space (1000 мс)")
        st.plotly_chart(fig_lat, use_container_width=True)

    with col_chart2:
        st.subheader("Радарна діаграма спроможностей C2")
        categories = ['Доступність (A)', 'Безперервність (C)', 'Норм. Затримка (f_L)', 'Цілісність (I)']
        values = [availability * 100, continuity * 100, f_L * 100, integrity * 100]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Поточний борт',
            line_color='#0F2C59'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[80, 80, 80, 80, 80],
            theta=categories + [categories[0]],
            name='Мінімальний поріг U-space',
            line_color='red',
            line_dash='dash'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
        st.plotly_chart(fig_radar, use_container_width=True)

with tab_sensitivity:
    st.subheader("Локалізація Parameter Bottlenecks")
    
    # Calculate sensitivity coefficients (+10% perturbation)
    delta = 0.10
    
    # Impact of Latency increase (+10% latency)
    f_L_perturbed = max(0.0, min(1.0, (L_max - mean_latency*1.10) / (L_max - l_threshold_ms)))
    R_C2_lat_change = (w_A*availability + w_C*continuity + w_L*f_L_perturbed + w_I*integrity) - R_C2
    
    # Impact of Packet Loss (+10% loss)
    avail_perturbed = max(0.0, 1.0 - packet_loss_rate*1.10)
    R_C2_loss_change = (w_A*avail_perturbed + w_C*continuity + w_L*f_L + w_I*integrity) - R_C2
    
    # Impact of Continuity drop (-10% continuity)
    cont_perturbed = continuity * 0.90
    R_C2_cont_change = (w_A*availability + w_C*cont_perturbed + w_L*f_L + w_I*integrity) - R_C2
    
    sens_df = pd.DataFrame({
        'Параметр': ['Затримка (Latency)', 'Втрата пакетів (Loss)', 'Безперервність (Continuity)'],
        'Вплив на R_C2 (%)': [R_C2_lat_change*100, R_C2_loss_change*100, R_C2_cont_change*100]
    })
    
    fig_sens = px.bar(
        sens_df, 
        x='Параметр', 
        y='Вплив на R_C2 (%)',
        color='Вплив на R_C2 (%)',
        color_continuous_scale='Reds_r',
        title="Коефіцієнти чутливості за варіації параметрів на +10%"
    )
    st.plotly_chart(fig_sens, use_container_width=True)

    # Automated Bottleneck Report Box
    st.markdown("### 📋 Bottleneck Diagnostic Report")
    
    if mean_latency > l_threshold_ms:
        st.warning(f"**🚨 Вузьке місце:** Середня затримка мережі ({mean_latency:.1f} мс) перевищує нормативний поріг U-space ({l_threshold_ms} мс).\n\n"
                   f"**🛠️ Рекомендована дія:** Підвищити частоту відправки телеметрії з {telemetry_freq_hz} Гц до 2.5–3.0 Гц або активувати QoS Slicing 5G.")
    elif packet_loss_rate > 0.03:
        st.warning(f"**🚨 Вузьке місце:** Рівень втрати пакетів ({packet_loss_rate*100:.2f}%) занадто високий для міського каньйону.\n\n"
                   f"**🛠️ Рекомендована дія:** Увімкнути дублювання телеметричного каналу (Multilink Satcom/LTE).")
    else:
        st.info("**✅ Стан C2-лінку задовільний:** Параметри затримок, втрат та доступності знаходяться в межах норми для обраного SAIL рівня.")

with tab_telemetry:
    st.subheader("Карта маршруту польоту БАС")
    st.map(df_telemetry[['lat', 'lon']].rename(columns={'lat': 'latitude', 'lon': 'longitude'}))
    
    st.subheader("Сирий фрагмент логу телеметрії")
    st.dataframe(df_telemetry.head(20))

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption("Магістерський дипломний проєкт KSE | Розробник: Студент ОП 'Безпілотні літальні апарати' | Спеціальність G12 (134)")
