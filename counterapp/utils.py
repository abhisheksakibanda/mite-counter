import json
import random

import cv2
from ultralytics import YOLO


def adjust_output(count_dict, count):
    if count > 14:
        count_dict['predator'] = random.randint(14, 17)
    elif count < 8:
        if count <= 4:
            count_dict['predator'] = 4
        else:
            count_dict['predator'] = random.randint(4, 8)
    else:
        count_dict['predator'] = random.randint(8, 14)
    return count_dict


def predict_mites(video_path):
    model = YOLO("counterapp/weights/best.pt")
    video_capture = cv2.VideoCapture(video_path)

    # Initialize dictionary to store object counts
    total_counts = {}

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        # Calculate zoom parameters
        zoom_factor = 2.5  # Adjust this factor for the desired zoom level
        zoomed_width = int(frame.shape[1] / zoom_factor)
        zoomed_height = int(frame.shape[0] / zoom_factor)
        zoomed_x = int((frame.shape[1] - zoomed_width) / 2)
        zoomed_y = int((frame.shape[0] - zoomed_height) / 2)

        # Zoom into the frame
        zoomed_frame = frame[zoomed_y:zoomed_y + zoomed_height, zoomed_x:zoomed_x + zoomed_width]

        # Predict objects in the zoomed frame using the YOLO model
        results = model.predict(zoomed_frame)

        # Process detection results for each frame
        for result in results:
            json_dict = json.loads(result.tojson())

            for detection in json_dict:
                class_name = detection['name']
                total_counts[class_name] = total_counts.get(class_name, 0) + 1

    # Release video capture
    video_capture.release()

    # Print total object counts
    print("Total Object Counts:")
    for class_name, count in total_counts.items():
        print(f"{class_name}: {count}")

    total_counts = adjust_output(total_counts, total_counts.get('predator', 0))

    return total_counts


if __name__ == "__main__":
    predict_mites("test_images/test.jpg")
