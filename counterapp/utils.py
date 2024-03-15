from ultralytics import YOLO


def predict_mites(img_source):
    model = YOLO("weights/best.pt")

    results = model.predict(source=img_source)
    return results


if __name__ == "__main__":
    predict_mites("test_images/test.jpg")
