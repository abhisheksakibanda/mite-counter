import json
import os

from django.core.files.images import ImageFile
from django.core.handlers.wsgi import WSGIRequest

import utils
from counterapp.models import Result


def predict(request: WSGIRequest, img_id: int) -> str:
    src_image = Result.objects.get(id=img_id).photo.image.path
    pred_results = utils.predict_mites(src_image)
    file_name = src_image.split("/")[-1]

    for result in pred_results:
        detect_count = dict()
        json_dict = json.loads(result.tojson())

        for detection in json_dict:
            detect_count[detection['name']] = detect_count.get(detection['name'], 0) + 1

        print('Detected Objects: ', detect_count)

        # Check if the results directory exists, if not create it
        if not os.path.exists("../results"):
            os.mkdir("../results")
        preds_img_path = result.save(filename=f"../results/{file_name}")

        result = Result.objects.create(
            obj_detection_image=ImageFile(open(preds_img_path, "rb")),
            feeder_mite_count=detect_count.get('feeder'),
            predator_mite_count=detect_count.get('predator'),
        )
        result.save()

        return json.dumps({
            'feeder_mite_count': detect_count.get('feeder'),
            'predator_mite_count': detect_count.get('predator'),
            'obj_detection_image': preds_img_path,
            'scan_date': result.scan_date
        })
