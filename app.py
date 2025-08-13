import streamlit as st
import time
import textwrap
import json
import random
from datetime import datetime
import plotly.graph_objects as go

# -------------------- Page Config & Minimal CSS --------------------
st.set_page_config(
    page_title="GDPR + NIS2 Compliance Architect (Agentic MVP)",
    page_icon="🛡️",
    layout="wide"
)

st.markdown(
    """
    <style>
      .title-box {
        background: linear-gradient(135deg,#0ea5e9, #22c55e);
        color: white; padding: 16px 20px; border-radius: 14px; 
        font-size: 24px; font-weight: 700; margin-bottom: 12px;
      }
      .subtle {
        color:#0f172a; opacity:0.85; font-size:15px;
      }
      .badge {
        display:inline-block; padding:6px 10px; border-radius:999px; 
        background:#f1f5f9; color:#0f172a; font-size:12px; margin-right:6px;
        border:1px solid #e2e8f0;
      }
      .red-box {
        display:inline-block; padding:10px 14px; border-radius:10px;
        background:#ef4444; color:white; font-weight:700; text-decoration:none;
      }
      .section {
        background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:16px;
      }
      .footer-card {
        background:#f8fafc; border:1px dashed #cbd5e1; border-radius:12px; padding:16px;
      }
      .pill {
        background:#eef2ff; color:#3730a3; border-radius:999px; padding:6px 10px; margin-right:8px;
        border:1px solid #e0e7ff; font-weight:600; font-size:12px;
      }
      .agent-name {
        font-weight:700; color:#111827;
      }
      .howto-step {
        padding:8px 12px; border-radius:10px; margin:6px 0; 
        border:1px solid #e5e7eb; background:#ffffff;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- Session State --------------------
if "last_architecture" not in st.session_state:
    st.session_state.last_architecture = ""
if "last_reports" not in st.session_state:
    st.session_state.last_reports = {}

# -------------------- Header --------------------
st.markdown('<div class="title-box">🛡️ GDPR + NIS2 Compliance Architect (Agentic MVP • 2050-ready)</div>', unsafe_allow_html=True)
st.caption("Builds compliance-first cloud designs. 90% focus: GDPR & NIS2. 10%: AWS/Data/DevOps mapping. No APIs. Free & open-source.")

colA, colB, colC = st.columns([1,1,1])
with colA:
    st.markdown('<span class="badge">GDPR</span> <span class="badge">NIS2</span>', unsafe_allow_html=True)
with colB:
    st.markdown('<span class="badge">AWS Mapping</span> <span class="badge">Data/DevOps</span>', unsafe_allow_html=True)
with colC:
    st.markdown('<span class="badge">Agentic AI (4 agents)</span> <span class="badge">Zero API</span>', unsafe_allow_html=True)

st.write(" ")

# -------------------- Sidebar: How to use & Reset --------------------
with st.sidebar:
    st.header("🧭 How to Use (Quick)")
    st.markdown(
        """
        1) Adjust the **6 sliders** (security, cost, etc.).  
        2) Type or paste your **Use Case / RFP / User Story**.  
        3) Click **Run Compliance + Design**.  
        4) Watch **4 agents** think like human architects.  
        5) See **Proposed Architecture** + **Reports**.  
        6) Use **Download** buttons to save outputs.  
        """
    )
    if st.button("🔄 Start New / Reset"):
        st.session_state.last_architecture = ""
        st.session_state.last_reports = {}
        st.experimental_rerun()

# -------------------- Radar Inputs (Sliders) --------------------
st.subheader("🎛️ Design Priorities (Adjustable Radar)")
left, right = st.columns([1,2])
with left:
    st.caption("Set what matters most for this solution.")
    latency = st.slider("Latency (lower is better)", 0, 10, 5)
    load_bal = st.slider("Load Balancing", 0, 10, 6)
    cost = st.slider("Cloud Cost", 0, 10, 5)
    perf = st.slider("Performance", 0, 10, 7)
    sec = st.slider("Security", 0, 10, 9)
    scale = st.slider("Scalability", 0, 10, 7)
with right:
    categories = ["Latency", "Load Balancing", "Cost", "Performance", "Security", "Scalability"]
    values = [latency, load_bal, cost, perf, sec, scale]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Priority"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,10])),
        showlegend=False,
        margin=dict(l=30, r=30, t=30, b=30),
        height=320
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------- Use Case Input --------------------
st.subheader("📝 Type or Paste Use Case / RFP / Epic User Story")
use_case = st.text_area(
    "Describe what you're building, data sensitivity, real-time aspects, sectors, etc.",
    height=140,
    placeholder="Example: We run a German healthcare analytics SaaS processing EU personal data in real time, storing pseudonymized records, training ML models, and alerting on anomalies..."
)

st.markdown(
    '<a class="red-box" href="#roi-section">Click Here to Know Architecture Value Chain ROI for Vendors & Clients</a>',
    unsafe_allow_html=True
)

# -------------------- Utilities --------------------
def contains_any(text, keywords):
    t = text.lower()
    return any(k in t for k in keywords)

def gdpr_rules(text):
    findings = []
    if contains_any(text, ["personal data", "patient", "pii", "email", "customer data", "user data", "health", "gdpr"]):
        findings += [
            "Lawful basis & consent where required (GDPR Art.6/7)",
            "Pseudonymization/Anonymization for analytics (Art.25, Art.32)",
            "Data Subject Rights workflows (access, delete, rectify) (Art.15–22)",
            "72-hour breach notification procedures (Art.33)",
            "Data Protection Impact Assessment (DPIA) if high-risk (Art.35)",
            "Data minimization & purpose limitation (Art.5)"
        ]
    if contains_any(text, ["ai", "ml", "model", "automl", "llm"]):
        findings += ["Document automated decision-making logic & human oversight (GDPR Art.22)"]
    if contains_any(text, ["cross-border", "usa", "india", "outside eu"]):
        findings += ["Assess international data transfers & SCCs where needed (Chapter V)"]
    if not findings:
        findings = ["No explicit personal data detected; still apply privacy-by-design (Art.25) as baseline."]
    return findings

def nis2_rules(text):
    findings = [
        "Risk management measures (policies, procedures, ownership)",
        "Security-by-design & encryption in transit/at rest",
        "Logging, monitoring, detection for incidents",
        "Incident reporting obligations to competent authorities (e.g., BSI in Germany)",
        "Business continuity & resilience planning",
        "Supply-chain security requirements"
    ]
    if contains_any(text, ["critical", "energy", "health", "transport", "water", "digital infrastructure", "telecom"]):
        findings.append("Sector likely in NIS2 scope → higher bar for governance & reporting.")
    if contains_any(text, ["real-time", "stream", "realtime"]):
        findings.append("Real-time telemetry → continuous monitoring & anomaly detection.")
    return list(dict.fromkeys(findings))  # unique order-preserving

def agent_think_simulation(lines, delay=0.15):
    # show a few steps with small delay (no external calls)
    holder = st.empty()
    text = ""
    for ln in lines:
        text += "• " + ln + "\n"
        holder.markdown(f"```\n{text}\n```")
        time.sleep(delay)
    return text

def aws_mapping(text, weights):
    # very small rule-based mapping influenced by security/perf/scale/cost
    sec_w, perf_w, scale_w, cost_w, lat_w, lb_w = weights
    components = []
    if sec_w >= 7:
        components += ["AWS KMS (encryption keys)", "VPC + Security Groups", "GuardDuty", "CloudTrail + CloudWatch Logs"]
    else:
        components += ["VPC + Security Groups", "CloudWatch Logs"]

    if perf_w >= 7 or lat_w >= 7:
        components += ["API Gateway + Lambda", "Amazon ElastiCache"]
    else:
        components += ["API Gateway + Lambda"]

    if scale_w >= 7 or lb_w >= 6:
        components += ["Application Load Balancer", "Auto Scaling"]

    if contains_any(text, ["stream", "real-time", "telemetry", "iot", "kinesis"]):
        components += ["Kinesis Data Streams", "Lambda ETL"]

    if contains_any(text, ["ml", "ai", "model", "predict"]):
        components += ["SageMaker (optional)"]

    # storage & analytics depending on cost/perf
    if cost_w >= 7:
        components += ["S3 Standard-IA (cost aware)", "Athena (serverless SQL)"]
    else:
        components += ["S3 (default)", "Athena or Redshift Serverless"]

    return list(dict.fromkeys(components))

def build_dot_diagram(components):
    # Always show Proposed Architecture (simple DOT to avoid system Graphviz)
    nodes = "\n".join([f'"{c}" [shape=box, style="rounded,filled", fillcolor="whitesmoke"]' for c in components])
    edges = []
    # naive chain
    for i in range(len(components)-1):
        edges.append(f'"{components[i]}" -> "{components[i+1]}"')
    dot = f"""
    digraph G {{
        rankdir=LR;
        node [fontname="Helvetica"];
        {nodes}
        {";".join(edges)}
    }}
    """
    return dot

def build_reports(use_case, gdpr_list, nis2_list, aws_list, priorities):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    sec_w, perf_w, scale_w, cost_w, lat_w, lb_w = priorities

    compliance_report = f"""
    GDPR + NIS2 Compliance Report
    Timestamp: {ts}

    Use Case:
    {use_case}

    --- GDPR Focus ---
    - {chr(10)+'- '.join(gdpr_list)}

    --- NIS2 Focus ---
    - {chr(10)+'- '.join(nis2_list)}

    --- Design Priorities (0-10) ---
    Security: {sec_w} | Performance: {perf_w} | Scalability: {scale_w} | Cost: {cost_w} | Latency: {lat_w} | Load Balancing: {lb_w}

    Notes:
    • This is a rules-driven MVP. For production, attach evidence (policies, DPIA, incident runbooks).
    """

    tdd = f"""
    Technical Design Document (TDD) - Proposed Architecture
    Timestamp: {ts}

    Use Case:
    {use_case}

    Components:
    - {chr(10)+'- '.join(aws_list)}

    Security Controls:
    - Encryption with KMS; IAM least-privilege; VPC isolation; GuardDuty detection; centralized logging.

    Data:
    - S3 object storage; Athena/Redshift serverless analytics; pseudonymization in ETL flows if personal data present.

    Operations:
    - CloudWatch metrics/logs; alerting; incident procedures aligned with NIS2; backup/restore plan.

    CI/CD:
    - Git-based workflow; build/test gates; infra-as-code (future extension).

    Limitations:
    - MVP heuristic, not legal advice. Validate with DPO/CISO.
    """

    tutorial = """
    Tutorial: How to Build This Architecture (Step-by-Step)
    1) Gather your use case & data classification (personal data? special categories?).
    2) Define priorities: security, latency, cost, performance, load balancing, scalability.
    3) Ingest data securely (HTTPS/API Gateway). Use VPC for isolation.
    4) Use IAM least-privilege for all roles and services.
    5) Encrypt data at rest with KMS; enforce TLS in transit.
    6) Store raw+processed data in S3; control access via bucket policies.
    7) For real-time, use Kinesis + Lambda to transform events.
    8) Pseudonymize or anonymize personal data before analytics (GDPR Art.25, Art.32).
    9) Query via Athena or Redshift Serverless (mask sensitive fields).
    10) Centralize logs with CloudWatch Logs; retain per compliance.
    11) Enable CloudTrail for audit trails; integrate GuardDuty for findings.
    12) Build anomaly alerts aligned with NIS2 incident response.
    13) Document breach process (72-hour reporting) and run tabletop drills.
    14) Version-control infra & app code in Git; add CI tests for configs.
    15) Tag resources for cost governance; review budgets & rightsizing.
    16) Prepare DPIA if high-risk processing; record decisions & mitigations.
    17) Implement data subject rights workflows (access/delete/rectify).
    18) Review suppliers (NIS2 supply chain); keep contracts & DPAs updated.
    19) Define RTO/RPO; test restore procedures periodically.
    20) Onboard a change process; update the TDD when architecture evolves.
    21) Localize policies for Germany; monitor regulator updates.
    """
    return compliance_report.strip(), tdd.strip(), tutorial.strip()

# -------------------- Agents (4) --------------------
def run_agents(use_case, priorities):
    sec_w, perf_w, scale_w, cost_w, lat_w, lb_w = priorities

    st.markdown("### 🤖 Agentic Analysis (Human-like)")

    # 1) Legal (GDPR) – Sophia
    with st.expander("👩‍⚖️ Legal Architect – Sophia (GDPR)", expanded=True):
        sophia_lines = [
            "Reading use case → identify personal data & special categories.",
            "Mapping GDPR Articles: lawful basis, minimization, DPIA, breach reporting.",
            "Recommending pseudonymization & rights workflows."
        ]
        sophia_thoughts = agent_think_simulation(sophia_lines)
        gdpr_list = gdpr_rules(use_case)

    # 2) Security (NIS2) – Emilia
    with st.expander("🛡️ Security Architect – Emilia (NIS2)", expanded=True):
        emilia_lines = [
            "Assessing sector/scope → is NIS2 applicable?",
            "Defining risk management, logging/monitoring, incident reporting.",
            "Recommending resilience & supply-chain checks."
        ]
        emilia_thoughts = agent_think_simulation(emilia_lines)
        nis2_list = nis2_rules(use_case)

    # 3) Cloud (AWS) – Kumar
    with st.expander("☁️ Cloud Architect – Kumar (AWS mapping)", expanded=True):
        kumar_lines = [
            "Converting compliance into cloud controls (KMS, IAM, VPC).",
            "Selecting serverless analytics based on priorities.",
            "Aligning real-time flows with Kinesis/Lambda if needed."
        ]
        kumar_thoughts = agent_think_simulation(kumar_lines)
        aws_list = aws_mapping(use_case, (sec_w, perf_w, scale_w, cost_w, lat_w, lb_w))

    # 4) Risk & Monitoring – Amit
    with st.expander("📈 Risk & Monitoring – Amit (Continuous compliance)", expanded=True):
        amit_lines = [
            "Designing continuous checks for logs, drift, and anomalies.",
            "Linking incidents to playbooks & reporting timelines.",
            "Suggesting evidence collection for audits."
        ]
        amit_thoughts = agent_think_simulation(amit_lines)

    return gdpr_list, nis2_list, aws_list

# -------------------- Main Action --------------------
st.write(" ")
col_run1, col_run2 = st.columns([1,3])
with col_run1:
    run = st.button("🚀 Run Compliance + Design", type="primary", use_container_width=True)
with col_run2:
    st.caption("This MVP is rules-based and offline. It demonstrates how autonomous compliance assistants could work by 2050.")

if run:
    if not use_case.strip():
        st.warning("Please enter a Use Case / RFP / User Story first.")
    else:
        # Agents
        gdpr_list, nis2_list, aws_list = run_agents(
            use_case,
            (sec, perf, scale, cost, latency, load_bal)
        )

        # Architecture
        st.subheader("🏗️ Proposed Architecture (Always Visible)")
        dot = build_dot_diagram(aws_list if aws_list else ["Input", "Processing", "Storage", "Analytics"])
        st.graphviz_chart(dot, use_container_width=True)

        # Reports
        comp_report, tdd_report, tutorial = build_reports(
            use_case, gdpr_list, nis2_list, aws_list,
            (sec, perf, scale, cost, latency, load_bal)
        )
        st.session_state.last_architecture = dot
        st.session_state.last_reports = {
            "Compliance Report.txt": comp_report,
            "Technical Design Document.txt": tdd_report,
            "Tutorial.txt": tutorial
        }

        st.subheader("📥 Downloads")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("⬇️ Compliance Report (TXT)", comp_report, file_name="Compliance_Report.txt")
        with c2:
            st.download_button("⬇️ Technical Design Doc (TXT)", tdd_report, file_name="Technical_Design_Document.txt")
        with c3:
            st.download_button("⬇️ Tutorial (TXT)", tutorial, file_name="Tutorial.txt")

# -------------------- ROI Section Anchor --------------------
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown('<h3 id="roi-section">💡 Architecture Value Chain ROI (Vendors & Clients)</h3>', unsafe_allow_html=True)
st.markdown(
    """
    - **Clients**: avoid fines, accelerate go-live, build trust, reduce audit time.  
    - **Vendors**: reusable compliance assets, faster delivery, clearer scope, lower support cost.  
    - **Shared**: transparency (who does what), measurable controls, repeatable patterns.
    """,
)

# -------------------- Detailed “How to Use” (Layman) --------------------
st.markdown("<hr/>", unsafe_allow_html=True)
st.subheader("📚 How to Use this Web App (Step-by-Step, Simple English)")
howto_steps = [
    "Look at the 6 sliders on top. Move them to show what matters most (e.g., Security high).",
    "Click into the big text box.",
    "Type your use case. Example: 'We store EU customer emails and stream telemetry in real-time.'",
    "If you handle personal data (names, emails), say it here.",
    "If your sector is critical (health, energy, water), mention it.",
    "Press the blue button: 'Run Compliance + Design'.",
    "Now watch four agents think like human architects.",
    "Sophia checks GDPR: consent, data rights, breach steps, DPIA.",
    "Emilia checks NIS2: risks, logging, reporting, resilience.",
    "Kumar maps to AWS: KMS, IAM, VPC, S3, Kinesis, Athena, etc.",
    "Amit adds monitoring & audits: logs, alerts, evidence.",
    "Scroll down to see the Proposed Architecture diagram.",
    "If it looks too simple, adjust the sliders and run again.",
    "Download your Compliance Report as TXT.",
    "Download your Technical Design Document (TDD) as TXT.",
    "Download the simple Tutorial as TXT.",
    "To start over, click 'Start New / Reset' in the left sidebar.",
    "Repeat for another use case (e.g., banking, e-commerce, IoT).",
    "If you mention 'AI/ML', the design will include ML options.",
    "If you mention 'real-time', the design will add streaming.",
    "If you mention 'cross-border', it adds transfer checks.",
    "Remember: this MVP is a helper; always consult legal/compliance specialists.",
    "Use the outputs to start real architecture work and audits.",
    "Keep records of your decisions (this helps audits later).",
    "If security is top priority, push the Security slider higher.",
    "If cost matters most, push the Cost slider higher.",
    "If you need high scale, increase Scalability and Load Balancing.",
    "Performance helps low-latency apps feel fast for users.",
    "Re-run until you get a good starting point for your team.",
    "Share the TXT reports with your manager or client.",
    "Save your TXT files as proof of your initial compliance design."
]
# nicer two-column layout
cols = st.columns(2)
for i, step in enumerate(howto_steps):
    with cols[i % 2]:
        st.markdown(f'<div class="howto-step"><b>Step {i+1}:</b> {step}</div>', unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)
st.info("This MVP is **offline** and **rules-based**. It demonstrates how, by 2050, autonomous compliance officers could run continuously and produce audit-ready evidence without manual effort.")

# -------------------- End --------------------
