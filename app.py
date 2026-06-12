import streamlit as st
import numpy as np
import time

from red_team import fuzzing
from blue_team import anomaly, defense_rules
from panels import attention, drift, introspection, mutation_timeline, replay_playback
from data import logger

# Course engines
from courses.bug_bounty_bootcamp.engine.engine import BugBountyEngine
from courses.docker_refresher.engine.engine import DockerRefresherEngine
from courses.powershell_refresher.engine.engine import PowerShellRefresherEngine
from courses.kali_refresher.engine.engine import KaliRefresherEngine
from courses.python_course.engine.engine import PythonCourseEngine

# Progress + activity systems
from data.progress import load_progress, add_xp, award_badge
from data.activity import log_activity, load_activity

# Initialize engines
bb_engine = BugBountyEngine()
docker_engine = DockerRefresherEngine()
ps_engine = PowerShellRefresherEngine()
kali_engine = KaliRefresherEngine()
python_engine = PythonCourseEngine()

print("All course engines loaded.")

# Streamlit UI
st.set_page_config(page_title="Red/Blue Hacking Cockpit", layout="wide")
st.title("🧠 Red/Blue Hacking Cockpit")

# Tabs for cockpit sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Red Team", "Blue Team", "Panels", "Courses", "Profile"]
)

# --- Red Team ---
with tab1:
    st.header("Red Team: Offensive Modules")
    token = fuzzing.fuzz_tokens()
    result = fuzzing.send_request(token)
    st.write("Single Fuzzing Result:", result)

    st.subheader("Batch Fuzzing")
    logs = [fuzzing.send_request(fuzzing.fuzz_tokens()) for _ in range(5)]
    st.write(logs)

# --- Blue Team ---
with tab2:
    st.header("Blue Team: Defensive Modules")
    logs = [fuzzing.send_request(fuzzing.fuzz_tokens()) for _ in range(10)]
    st.write("Incoming Events:", logs)

    st.subheader("Defense Decisions")
    for event in logs:
        decisions = defense_rules.apply_rules(event)
        st.write(event, "→", decisions)
        logger.log_fuzz_event(event)

    st.subheader("Anomaly Detection")
    df = anomaly.detect_anomalies(logs)
    st.write(df)

    st.subheader("Rule Mutations")
    mutations = defense_rules.evolve_rules()
    st.write(mutations)
    for m in mutations:
        logger.log_mutation(m)

# --- Panels ---
with tab3:
    st.header("Cockpit Panels")

    st.subheader("Attention Overlay")
    attention.show_attention(df)

    st.subheader("Drift Tracker")
    drift.show_drift([{"rule": "entropy>4", "mutation": "lowered to 3.5"}])

    st.subheader("Multi-Agent Introspection")
    introspection.compare_agents(["Allowed", "Blocked"], ["Suspicious", "Allowed"])

    st.subheader("Mutation Timeline")
    mutation_timeline.show_mutation_timeline(mutations)

    st.subheader("Replay & Playback")
    replay_playback.show_replay_playback()

# --- Courses ---
with tab4:
    st.header("📚 Training Courses")

    progress = load_progress()

    # --- Profile / Progress ---
    st.subheader("Your Progress")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Level", progress["level"])
    with col2:
        st.metric("XP", progress["xp"])

    # XP bar toward next level
    next_level_xp = progress["level"] * 100
    st.progress(min(progress["xp"] / next_level_xp, 1.0))

    if progress["badges"]:
        st.write("**Badges:**")
        for b in progress["badges"]:
            st.markdown(f"- 🏅 {b}")
    else:
        st.write("**Badges:** None yet")

    st.divider()

    # --- Course Runner ---
    course = st.selectbox(
        "Choose a course:",
        [
            "Bug Bounty Bootcamp",
            "Docker Refresher",
            "PowerShell Refresher",
            "Kali Linux Refresher",
            "Python Course"
        ]
    )

    # Engine selection
    if course == "Bug Bounty Bootcamp":
        engine = bb_engine
        max_modules = 10
    elif course == "Docker Refresher":
        engine = docker_engine
        max_modules = 10
    elif course == "PowerShell Refresher":
        engine = ps_engine
        max_modules = 10
    elif course == "Kali Linux Refresher":
        engine = kali_engine
        max_modules = 10
    elif course == "Python Course":
        engine = python_engine
        max_modules = 20

    module_id = st.number_input("Module ID", min_value=1, max_value=max_modules, step=1)

    if st.button("Run Module"):
        st.write(f"### Running {course} — Module {module_id}")
        engine.run_module(module_id)

        # Log activity
        log_activity(course, int(module_id))

        # XP reward
        xp_gain = 20
        before = load_progress()
        before_level = before["level"]

        updated = add_xp(xp_gain)
        st.success(f"+{xp_gain} XP earned!")

        # Level-up celebration
        if updated["level"] > before_level:
            st.success(f"🎉 Level Up! You are now Level {updated['level']}")
            st.balloons()

        # Badge logic
        if updated["level"] >= 5 and "Level 5 Hacker" not in updated["badges"]:
            award_badge("Level 5 Hacker")
            st.success("🏅 New Badge: Level 5 Hacker")

        if module_id == 1 and "First Steps" not in updated["badges"]:
            award_badge("First Steps")
            st.success("🏅 New Badge: First Steps")

        st.write(f"**Current Level:** {updated['level']}")
        st.write(f"**XP toward next level:** {updated['xp']} / {updated['level'] * 100}")

# --- Profile ---
with tab5:
    st.header("🛰 Operator Profile Dashboard")

    progress = load_progress()
    activity = load_activity()

    # --- Holographic Neon Side Frames ---
    frame_left, frame_center, frame_right = st.columns([1, 6, 1])

    with frame_left:
        st.markdown("### 🔷")
        size = 80
        x = np.linspace(0, 6*np.pi, size)
        y = np.linspace(0, 6*np.pi, size)
        X, Y = np.meshgrid(x, y)

        left_frame = (
            np.sin(X * 0.5 + time.time() * 3) * 0.4 +
            np.cos(Y * 2 + time.time() * 1.5) * 0.6
        )
        left_frame = (left_frame - left_frame.min()) / (left_frame.max() - left_frame.min() + 1e-8)
        st.image(left_frame, use_column_width=True)

    with frame_right:
        st.markdown("### 🔶")
        size = 80
        x = np.linspace(0, 6*np.pi, size)
        y = np.linspace(0, 6*np.pi, size)
        X, Y = np.meshgrid(x, y)

        right_frame = (
            np.cos(X * 0.5 + time.time() * 2.5) * 0.4 +
            np.sin(Y * 2 + time.time() * 1.2) * 0.6
        )
        right_frame = (right_frame - right_frame.min()) / (right_frame.max() - right_frame.min() + 1e-8)
        st.image(right_frame, use_column_width=True)

    # --- Operator Rank ---
    st.subheader("Operator Rank")

    level = progress["level"]

    if level < 5:
        rank = "Recruit"
    elif level < 10:
        rank = "Field Operative"
    elif level < 20:
        rank = "Senior Operator"
    elif level < 30:
        rank = "Cyber Tactician"
    else:
        rank = "Shadow Architect"

    st.markdown(f"### 🎖 {rank}")

    # --- XP + Level HUD ---
    st.subheader("XP & Level Status")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Level", progress["level"])
    with col2:
        st.metric("XP", progress["xp"])

    next_level_xp = progress["level"] * 100
    st.progress(min(progress["xp"] / next_level_xp, 1.0))

    # --- Hex Matrix + 3D Sphere (side-by-side) ---
    st.subheader("Holographic Network Visuals")
    holo_left, holo_right = st.columns(2)

    with holo_left:
        st.markdown("**Hex‑Matrix Hologram**")
        grid_size = 20
        x = np.linspace(0, 2*np.pi, grid_size)
        y = np.linspace(0, 2*np.pi, grid_size)
        X, Y = np.meshgrid(x, y)

        flicker = (np.sin(X * 3 + time.time() * 4) +
                   np.cos(Y * 3 + time.time() * 4)) * 0.5 + 0.5
        st.image(flicker, caption="Live Hex‑Matrix Network Topology", use_column_width=True)

    with holo_right:
        st.markdown("**3D Network Sphere Hologram**")
        sphere_size = 60
        theta = np.linspace(0, 2*np.pi, sphere_size)
        phi = np.linspace(0, np.pi, sphere_size)
        T, P = np.meshgrid(theta, phi)

        Xs = np.sin(P) * np.cos(T)
        Ys = np.sin(P) * np.sin(T)
        Zs = np.cos(P)

        t = time.time()
        distort = 0.2 * np.sin(4*T + t) * np.cos(3*P + t)
        Z_holo = Zs + distort

        holo_sphere = (Z_holo - Z_holo.min()) / (Z_holo.max() - Z_holo.min() + 1e-8)
        st.image(holo_sphere, caption="Rotating Network Sphere Hologram", use_column_width=True)

    # --- Biometrics + Threat Intel (side-by-side) ---
    st.subheader("Operator State & Threat Intel")
    bio_col, threat_col = st.columns(2)

    with bio_col:
        st.markdown("### Operator Biometrics")

        bio1, bio2, bio3 = st.columns(3)

        with bio1:
            st.markdown("**Pulse**")
            t = np.linspace(0, 2*np.pi, 200)
            pulse_wave = np.abs(np.sin(4*t + time.time()*3)) * 0.8
            st.line_chart(pulse_wave)

        with bio2:
            st.markdown("**Stress Level**")
            stress = int((np.sin(time.time()*0.7) + 1) * 50)
            st.progress(stress / 100)
            st.write(f"{stress}%")

        with bio3:
            st.markdown("**Focus Stability**")
            focus = (np.cos(time.time()*0.9) + 1) / 2
            st.progress(focus)
            st.write(f"{int(focus * 100)}%")

    with threat_col:
        st.markdown("### Threat‑Intel Hologram")

        intel1, intel2 = st.columns(2)

        with intel1:
            st.markdown("**Threat Level**")
            threat = int((np.sin(time.time()*1.3) + 1) * 50)
            st.progress(threat / 100)
            st.write(f"{threat}%")

        with intel2:
            st.markdown("**Threat Vector Radar**")
            size = 40
            x = np.linspace(0, 4*np.pi, size)
            y = np.linspace(0, 4*np.pi, size)
            X, Y = np.meshgrid(x, y)

            radar = (np.sin(X + time.time()*2) * np.cos(Y + time.time()*3))
            radar = (radar - radar.min()) / (radar.max() - radar.min() + 1e-8)
            st.image(radar, use_column_width=True)

        st.markdown("**Attack Surface Heatmap**")
        heat = np.random.rand(20, 20) * (0.5 + 0.5*np.sin(time.time()))
        st.image(heat, use_column_width=True)

        st.markdown("**Live Threat Score**")
        threat_score = (np.sin(time.time()*2) + 1) / 2
        st.progress(threat_score)
        st.write(f"{int(threat_score * 100)}%")

    # --- Badges + Activity (side-by-side) ---
    st.subheader("Achievements & Activity")
    badge_col, activity_col = st.columns(2)

    with badge_col:
        st.markdown("### Badge Wall")
        if progress["badges"]:
            for b in progress["badges"]:
                st.markdown(f"- 🏅 **{b}**")
        else:
            st.write("No badges earned yet.")

    with activity_col:
        st.markdown("### Recent Activity")
        if activity:
            for entry in reversed(activity[-10:]):
                st.markdown(
                    f"**{entry['timestamp']}** — Ran *{entry['course']}* Module {entry['module']}"
                )
        else:
            st.write("No activity recorded yet.")
