import cv2
from recognition import model, load_students, recognize_face

students = load_students()

image = cv2.imread("assets/classroom_images/classroom_test.png")
faces = model.get(image)

print(f"\nFaces detected: {len(faces)}\n")

for i, face in enumerate(faces, 1):
    name, score = recognize_face(face.embedding, students)

    print(f"Face {i}: {name} ({score:.2%})")