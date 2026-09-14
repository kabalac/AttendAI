import cv2
import insightface
import numpy as np
from pathlib import Path


STUDENTS_DIR = Path("data/students")


# Load AI model
model = insightface.app.FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

model.prepare(ctx_id=0, det_size=(640, 640))


def get_face_embedding(image_path):
    image = cv2.imread(str(image_path))

    if image is None:
        return None

    faces = model.get(image)

    if not faces:
        return None

    # Use the largest detected face
    face = max(faces, key=lambda f: f.bbox[2] - f.bbox[0])

    return face.embedding


def load_students():
    students = {}

    for student_folder in STUDENTS_DIR.iterdir():

        if not student_folder.is_dir():
            continue

        embeddings = []

        for image_path in student_folder.glob("*"):
            if image_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:

                embedding = get_face_embedding(image_path)

                if embedding is not None:
                    embeddings.append(embedding)

        if embeddings:
            students[student_folder.name] = np.mean(embeddings, axis=0)

    return students


def recognize_face(face_embedding, students, threshold=0.45):

    best_student = "Unknown"
    best_score = 0

    for student_name, student_embedding in students.items():

        similarity = np.dot(face_embedding, student_embedding) / (
            np.linalg.norm(face_embedding)
            * np.linalg.norm(student_embedding)
        )

        if similarity > best_score:
            best_score = similarity
            best_student = student_name

    if best_score < threshold:
        return "Unknown", best_score

    return best_student, best_score