import json
import os

from django.core.files.images import ImageFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect

from counterapp import utils
from counterapp.models import Result
from growlivapp.models import Photo
from mitecountpro import settings


def predict(request: WSGIRequest, img_id: int) -> HttpResponse:
    src_image = Photo.objects.get(id=img_id)
    pred_results = utils.predict_mites(src_image.image.path)
    file_name = os.path.basename(src_image.image.path)

    for result in pred_results:
        detect_count = dict()
        json_dict = json.loads(result.tojson())

        for detection in json_dict:
            detect_count[detection['name']] = detect_count.get(detection['name'], 0) + 1

        print('Detected Objects: ', detect_count)

        save_path = os.path.join(settings.MEDIA_ROOT, file_name)
        result.save(filename=save_path)

        pred_result = Result.objects.create(
            obj_detection_image=ImageFile(open(f"media/{file_name}", "rb")),
            feeder_mite_count=detect_count.get('feeder', 0),
            predator_mite_count=detect_count.get('predator', 0),
            photo_id=img_id
        )
        pred_result.save()
        return redirect('growlivapp:scan_detail_page')
