import cv2
from recognition import model, load_students, recognize_face

IMAGE_PATH = "assets/classroom_images/classroom_test.png"
OUTPUT_PATH = "assets/classroom_images/result.jpg"

students = load_students()

image = cv2.imread(IMAGE_PATH)
faces = model.get(image)

for face in faces:
    name, score = recognize_face(face.embedding, students)

    x1, y1, x2, y2 = map(int, face.bbox)

    # Green = recognized, Red = unknown
    color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    label = f"{name} {score:.0%}"

    cv2.putText(
        image,
        label,
        (x1, max(y1 - 10, 20)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2
    )

cv2.imwrite(OUTPUT_PATH, image)

print(f"Result saved to: {OUTPUT_PATH}")