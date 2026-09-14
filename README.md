# 🛸 U-space C2 Readiness Diagnostic Validator

**B2B-платформа передпольотної діагностики та оцінювання готовності C2-лінку БАС до польотів у повітряному просторі U-space (за вимогами Regulation EU 2021/664)**

Магістерський дипломний проєкт Інженерної школи **Київської школи економіки (KSE)**  
Спеціальність: **G12 (134) «Авіаційна та ракетно-космічна техніка»**  
Освітньо-професійна програма: **«Безпілотні літальні апарати»**

---

## 📌 Про проблему та рішення
При отриманні дозволів на польоти у міських геозонах U-space (**Flight Authorisation**) комерційні оператори БАС стикаються з невизначеністю вимог провайдерів U-space (**USSP**). 

**U-space Readiness Validator** — це легкий B2B інструмент експрес-діагностики, який:
1. Завантажує польотний лог телеметрії БАС (`.csv`, MAVLink).
2. Розраховує інтегральний показник технічної готовності C2-лінку ($R_{C2}$) на основі $A$ (Availability), $C$ (Continuity), $L$ (Latency) та $I$ (Integrity).
3. Проводить аналіз чутливості (Sensitivity Analysis) та виявляє параметрні **«вузькі місця» (Bottleneck Diagnostic Report)**.
4. Надає оператору чіткі інженерні рекомендації для коригування конфігурації борту до вильоту.

---

## 🚀 Швидкий запуск (Quick Start)

### 1. Клонування репозиторію
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Встановлення необхідних бібліотек
```bash
pip install streamlit pandas numpy plotly
```

### 3. Запуск веб-додатка у браузері
```bash
streamlit run app.py
```
Після запуску додаток автоматично відкриється у браузері за адресою: `http://localhost:8501`.

---

## 📁 Структура репозиторію
```text
├── app.py                      # Головний файл веб-додатка на Streamlit
├── flight_telemetry_log.csv    # Демонстраційний лог телеметрії міської місії БАС
├── requirements.txt            # Перелік залежностей Python
└── README.md                   # Документація проєкту
```

---

## 📦 Вміст requirements.txt
```text
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
```

---

## 📑 Нормативна база
* **Regulation (EU) 2021/664** (Regulatory framework for U-space)
* **EASA Easy Access Rules for U-space** (ED Decision 2022/022/R)
* **JARUS Required C2 Link Performance (RLP) Concept**
* **SORA 2.5 (Specific Operations Risk Assessment)**
