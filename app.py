import streamlit as st
import cv2
import numpy as np
import pandas as pd
from io import BytesIO
from datetime import datetime

from recognition import model, load_students, recognize_face


st.set_page_config(
    page_title="AttendAI",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        background: #f5f7fa;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🎓 AttendAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered classroom attendance from a single photograph</div>',
    unsafe_allow_html=True
)

st.divider()

students = load_students()

col1, col2 = st.columns(2)

with col1:
    class_name = st.text_input(
        "Class",
        value="CSE - 7th Semester"
    )

with col2:
    subject = st.text_input(
        "Subject",
        value="Deep Learning & NLP"
    )

uploaded_file = st.file_uploader(
    "Upload a classroom photo",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    if st.button("🔍 Analyze Attendance", type="primary"):

        with st.spinner("Analyzing classroom image..."):

            faces = model.get(image)

            attendance = {
                student: "Absent"
                for student in students
            }

            results = []

            for face in faces:

                name, score = recognize_face(
                    face.embedding,
                    students
                )

                x1, y1, x2, y2 = map(
                    int,
                    face.bbox
                )

                if name != "Unknown":
                    attendance[name] = "Present"
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                cv2.rectangle(
                    image,
                    (x1, y1),
                    (x2, y2),
                    color,
                    2
                )

                cv2.putText(
                    image,
                    f"{name} {score:.0%}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

                results.append({
                    "Student": name,
                    "Confidence": f"{score:.1%}"
                })

            image_rgb = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    image_rgb,
                    caption="AI Recognition Result",
                    width="stretch"
                )

            with col2:

                present = list(attendance.values()).count("Present")
                total = len(students)
                percentage = (present / total) * 100
                unknown_faces = sum(
                    1 for result in results
                    if result["Student"] == "Unknown"
                )   

                st.metric(
                    "👤 Registered Present",
                    f"{present}/{total}"
                )

                st.metric(
                    "📊 Attendance",
                    f"{percentage:.0f}%"
                )

                st.metric(
                    "❓ Unknown Faces",
                    unknown_faces
                )

                st.divider()
                st.success(
                    f"Attendance processed successfully for {class_name} — {subject}"
                )

                students_df = pd.read_csv("data/students/students.csv")

                attendance_rows = []

                for _, student in students_df.iterrows():
                    folder_name = f"{student['id']}_{student['name'].replace(' ', '_')}"

                    attendance_rows.append({
                        "Name": student["name"],
                        "Roll Number": student["roll_number"],
                        "Status": "🟢 Present" if attendance.get(folder_name) == "Present" else "🔴 Absent",
                        "Class": class_name,
                        "Subject": subject,
    "Date": datetime.now().strftime("%d-%m-%Y"),
        "Time": datetime.now().strftime("%I:%M %p")
    })

                attendance_df = pd.DataFrame(attendance_rows)
                st.dataframe(
                    attendance_df,
                    width="stretch",
                    hide_index=True
                )


                csv = attendance_df.to_csv(index=False)

                safe_class = class_name.replace(" ", "_").replace("/", "-")
                safe_subject = subject.replace(" ", "_").replace("/", "-")
                date_str = datetime.now().strftime("%d-%m-%Y")

                filename = f"Attendance_{safe_class}_{safe_subject}_{date_str}.csv"

                st.download_button(
                    "📥 Download CSV",
                    csv,
                    filename,
                    "text/csv"
                )       

            
                

                excel_buffer = BytesIO()

                attendance_df.to_excel(
                    excel_buffer,
                    index=False,
                    engine="openpyxl"
                )

                st.download_button(
                    "📊 Download Excel",
                    excel_buffer.getvalue(),
                    filename.replace(".csv", ".xlsx"),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )        