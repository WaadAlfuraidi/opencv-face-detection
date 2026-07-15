from pathlib import Path

import cv2


# تحديد موقع مجلد المشروع
project_folder = Path(__file__).resolve().parent

# تحديد مسارات الملفات
image_path = project_folder / "Face.jpg"
cascade_path = project_folder / "haarcascade_frontalface_default.xml"
result_path = project_folder / "Result.jpg"


# تحميل الصورة
image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(
        "Face.jpg was not found. Make sure it is in the same project folder."
    )


# تحميل نموذج اكتشاف الوجوه
face_detector = cv2.CascadeClassifier(str(cascade_path))

if face_detector.empty():
    raise FileNotFoundError(
        "The Haar Cascade XML file could not be loaded."
    )


# تحويل الصورة من ملونة إلى رمادية
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# اكتشاف الوجوه في الصورة
faces = face_detector.detectMultiScale(
    gray_image,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(40, 40)
)


# رسم مربع واسم حول كل وجه
for face_number, (x, y, width, height) in enumerate(faces, start=1):

    cv2.rectangle(
        image,
        (x, y),
        (x + width, y + height),
        (0, 255, 0),
        2
    )

    cv2.putText(
        image,
        f"Face {face_number}",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


# كتابة عدد الوجوه على الصورة
cv2.putText(
    image,
    f"Detected Faces: {len(faces)}",
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 0, 255),
    2
)


# حفظ صورة النتيجة
saved_successfully = cv2.imwrite(str(result_path), image)

if not saved_successfully:
    raise RuntimeError("The result image could not be saved.")


# طباعة النتيجة في Terminal
print("Face detection completed successfully.")
print(f"Number of detected faces: {len(faces)}")
print(f"Result saved as: {result_path.name}")


# عرض الصورة
cv2.imshow("Face Detection Result", image)

print("Press any key on the image window to close it.")

cv2.waitKey(0)
cv2.destroyAllWindows()