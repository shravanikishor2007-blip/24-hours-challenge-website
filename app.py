import streamlit as st
from datetime import datetime, timedelta
import random
import sqlite3

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="24 Hours Wellness Challenge",
    layout="wide"
)

# ---------------- DATABASE ----------------

conn = sqlite3.connect("wellness.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    task_name TEXT,
    category TEXT,
    task_time TEXT,
    done INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS journal(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry TEXT
)
""")


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
.big-title {
    text-align: center;
    color: #6C63FF;
    font-size: 55px;
    font-weight: bold;
}

.quote {
    text-align: center;
    color: #444;
    font-size: 22px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    "<div class='big-title'>🌟 24 Hours Wellness Challenge</div>",
    unsafe_allow_html=True
)

quotes = [
    "Small progress is still progress 💪",
    "Your future is created today 🌱",
    "Take care of your mind and body 🧘",
    "Creativity takes courage 🎨",
    "Discipline beats motivation 🔥"
]

st.markdown(
    f"<div class='quote'>{random.choice(quotes)}</div>",
    unsafe_allow_html=True
)

# ---------------- USER INPUT ----------------

name = st.text_input("👤 Enter Your Name")

if not name:
    st.warning("Please enter your name first")
    st.stop()

st.success(f"Welcome {name}! Let's make today productive ✨")

# ---------------- TIMER ----------------

st.subheader("⏰ 24 Hour Challenge Timer")

if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

start_time = st.session_state.start_time
end_time = start_time + timedelta(hours=24)

remaining = end_time - datetime.now()

if remaining.total_seconds() > 0:

    hours, remainder = divmod(
        int(remaining.total_seconds()), 3600
    )

    minutes, seconds = divmod(remainder, 60)

    st.markdown(
        f"""
        <h1 style='text-align:center;
                   color:#FF4B4B;
                   font-size:70px;'>
        {hours:02}:{minutes:02}:{seconds:02}
        </h1>
        """,
        unsafe_allow_html=True
    )

else:
    st.success("🎉 24 Hour Challenge Completed!")
# ---------------- ADD TASK ----------------

st.subheader("➕ Add Your Own Task")

task_name = st.text_input("Task Name")

category = st.selectbox(
    "Category",
    ["Study", "Health", "Exercise", "Reading", "Creative"]
)

task_time = st.time_input("Select Time")

if st.button("Add Task"):

    if task_name.strip() != "":

        cursor.execute(
    """
    INSERT INTO tasks
    (user_name, task_name, category, task_time)
    VALUES (?, ?, ?, ?)
    """,
    (name, task_name, category, str(task_time))
)
conn.commit()

# ---------------- DAILY TIMETABLE ----------------

st.subheader("📋 My Daily Timetable")

cursor.execute("""
SELECT id, task_name, category, task_time, done
FROM tasks
WHERE user_name = ?
ORDER BY task_time
""", (name,))

saved_tasks = cursor.fetchall()

if len(saved_tasks) == 0:

    st.info("No tasks added yet")

else:

    for task in saved_tasks:

        task_id = task[0]

        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

        col1.write(f"📌 {task[1]}")
        col2.write(task[2])
        col3.write(task[3])

        if task[4] == 0:

            if col4.button("Done ✅", key=f"done_{task_id}"):

                cursor.execute(
                    """
                    UPDATE tasks
                    SET done = 1
                    WHERE id = ?
                    """,
                    (task_id,)
                )

                conn.commit()
                st.rerun()

        else:
            col4.write("🏆")

# ---------------- WELLNESS TASKS ----------------

st.subheader("✅ Today's Wellness Challenges")

wellness_tasks = [
    "📚 Study for 2 Hours",
    "💧 Drink 8 Glasses of Water",
    "🏃 Exercise for 30 Minutes",
    "🧘 Meditate for 10 Minutes",
    "🎨 Create Something Creative",
    "📖 Read 20 Pages",
    "😊 Write 3 Gratitude Notes",
    "😴 Sleep Before 11 PM"
]

completed = 0

for task in wellness_tasks:

    if st.checkbox(task):
        completed += 1

# ---------------- PROGRESS ----------------

progress = completed / len(wellness_tasks)

st.subheader("📈 Your Progress")

st.progress(progress)

st.metric(
    "Completion",
    f"{int(progress * 100)}%"
)

# ---------------- CREATIVE TASK CATEGORIES ----------------

creative_categories = {
    "Art & Design": [
        "Drawing",
        "Painting",
        "Sketching",
        "Doodle Art",
        "Poster Making",
        "Logo Design",
        "Other"
    ],

    "Writing": [
        "Essay Writing",
        "Poem Writing",
        "Story Writing",
        "Journal Writing",
        "Write a Motivational Quote",
        "Letter to Future Self",
        "Other"
    ],

    "Learning & Knowledge": [
        "Read a Book for 20 Minutes",
        "Learn 10 New English Words",
        "Watch an Educational Video",
        "Solve a Puzzle",
        "Learn a Science Fact",
        "Learn a New Skill",
        "Other"
    ],

    "Public Speaking": [
        "Speak on a Topic for 2 Minutes",
        "Practice a Presentation",
        "Record a Speech",
        "Read Aloud",
        "Improve Pronunciation",
        "Other"
    ],

    "Creativity & Innovation": [
        "Think of a New App Idea",
        "Design a Smart Product",
        "Create a Business Idea",
        "Solve a Daily-Life Problem",
        "Brainstorm New Inventions",
        "Other"
    ],

    "Technology": [
        "Practice Python Coding",
        "Learn a New Programming Concept",
        "Create a Simple Project",
        "Explore an AI Tool",
        "Learn Keyboard Shortcuts",
        "Other"
    ]
}

# ---------------- DROPDOWN MENUS ----------------

selected_category = st.selectbox(
    "🎨 Select Creative Category",
    list(creative_categories.keys())
)

selected_task = st.selectbox(
    "✨ Select Creative Task",
    creative_categories[selected_category]
)

# If user selects Other, allow custom input
if selected_task == "Other":
    custom_task = st.text_input(
        "✍️ Enter Your Creative Task"
    )

    if custom_task:
        st.success(
            f"Selected Category: {selected_category}\n\nCustom Task: {custom_task}"
        )
else:
    st.success(
        f"Selected Category: {selected_category}\n\nSelected Task: {selected_task}"
    )
# ---------------- WELLNESS SCORE ----------------

score = int(progress * 100)

st.subheader("🏆 Wellness Score")

if score == 100:
    st.balloons()
    st.success("🏅 Perfect Day! You completed everything!")

elif score >= 70:
    st.success("🔥 Excellent work today!")

elif score >= 40:
    st.info("🌱 Good progress! Keep improving.")

else:
    st.warning("⚡ Start small and stay consistent!")

if st.button("Save Journal"):

    if journal.strip() != "":

        cursor.execute(
            """
            INSERT INTO journal(user_name, entry)
            VALUES (?, ?)
            """,
            (name, journal)
        )

        conn.commit()

        st.success("Journal Saved Successfully ✅")
st.subheader("📚 My Previous Journals")

cursor.execute("""
SELECT entry
FROM journal
WHERE user_name = ?
ORDER BY id DESC
""", (name,))

entries = cursor.fetchall()

if entries:
    for entry in entries:
        st.write("•", entry[0])

# ---------------- FOOTER ----------------

st.write("---")

st.markdown(
    "<center>Made with ❤️ for Student Wellness & Growth</center>",
    unsafe_allow_html=True
)