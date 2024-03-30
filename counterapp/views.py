from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect

from counterapp import utils
from counterapp.models import Result
from growlivapp.models import Video


def predict(request: WSGIRequest, video_id: int) -> HttpResponse:
    src_video = Video.objects.get(id=video_id)
    pred_results = utils.predict_mites(src_video.video.path)

    pred_result = Result.objects.create(
        feeder_mite_count=pred_results.get('feeder', 0),
        predator_mite_count=pred_results.get('predator', 0),
        video_id=video_id
    )
    pred_result.save()
    return redirect('growlivapp:scan_detail_page')
