import json
import logging

from django.http import JsonResponse
from django.shortcuts import redirect, render 

from .decorators import model_login_required
from .models import InferenceHistory
from .services.sentiment import run_sentiment
from .services.summarizer import run_summarize
from .services.moderator import run_moderate
from .services.combo import run_combo

logger = logging.getLogger(__name__)

SENTIMENT_MIN_LEN = 1
SENTIMENT_MAX_LEN = 1000

SUMMARIZE_MIN_LEN = 100
SUMMARIZE_MAX_LEN = 5000

MODERATE_MIN_LEN = 1
MODERATE_MAX_LEN = 1000

COMBO_MIN_LEN = 200
COMBO_MAX_LEN = 5000


def home(request):
    return redirect("my_gpt:sentiment")

def sentiment_view(request):
    histories = []
    if request.user.is_authenticated:
        histories = (
            InferenceHistory.objects
            .filter(user=request.user, task=InferenceHistory.Task.SENTIMENT)
            .order_by("-created_at")[:5]
        )
    return render(request, "my_gpt/sentiment.html", {"histories": histories})

def sentiment_run(request):
    if request.method != "POST":
        return JsonResponse({"error": "허용되지 않은 요청입니다."}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)

    text = body.get("text", "")

    if not isinstance(text, str):
        return JsonResponse({"error": "잘못된 입력값입니다."}, status=400)

    if not text.strip():
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)

    if len(text) < SENTIMENT_MIN_LEN or len(text) > SENTIMENT_MAX_LEN:
        return JsonResponse(
            {"error": f"문장은 {SENTIMENT_MIN_LEN:,}자 이상 {SENTIMENT_MAX_LEN:,}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = run_sentiment(text)
    except Exception:
        logger.exception("Sentiment inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    if request.user.is_authenticated:
        InferenceHistory.objects.create(
            user=request.user,
            task=InferenceHistory.Task.SENTIMENT,
            input_text=text,
            output_text=result["label"],
            result_data=result,
        )

    return JsonResponse(result)


@model_login_required
def summarize_view(request):
    histories = (
        InferenceHistory.objects
        .filter(user=request.user, task=InferenceHistory.Task.SUMMARIZE)
        .order_by("-created_at")[:5]
    )
    return render(request, "my_gpt/summarize.html", {"histories": histories})


@model_login_required
def summarize_run(request):
    if request.method != "POST":
        return JsonResponse({"error": "허용되지 않은 요청입니다."}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)

    text = body.get("text", "")

    if not isinstance(text, str):
        return JsonResponse({"error": "잘못된 입력값입니다."}, status=400)

    if not text.strip():
        return JsonResponse({"error": "요약할 문서를 입력해주세요."}, status=400)

    if len(text) < SUMMARIZE_MIN_LEN:
        return JsonResponse(
            {"error": f"요약할 문서는 {SUMMARIZE_MIN_LEN:,}자 이상 입력해주세요."},
            status=400,
        )

    if len(text) > SUMMARIZE_MAX_LEN:
        return JsonResponse(
            {"error": f"문서는 {SUMMARIZE_MAX_LEN:,}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = run_summarize(text)
    except Exception:
        logger.exception("Summarize inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.SUMMARIZE,
        input_text=text,
        output_text=result["summary"],
        result_data=result,
    )

    return JsonResponse(result)


@model_login_required
def moderate_view(request):
    histories = (
        InferenceHistory.objects
        .filter(user=request.user, task=InferenceHistory.Task.MODERATE)
        .order_by("-created_at")[:5]
    )
    return render(request, "my_gpt/moderate.html", {"histories": histories})


@model_login_required
def moderate_run(request):
    if request.method != "POST":
        return JsonResponse({"error": "허용되지 않은 요청입니다."}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)

    text = body.get("text", "")

    if not isinstance(text, str):
        return JsonResponse({"error": "잘못된 입력값입니다."}, status=400)

    if not text.strip():
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)

    if len(text) < MODERATE_MIN_LEN or len(text) > MODERATE_MAX_LEN:
        return JsonResponse(
            {"error": f"문장은 {MODERATE_MIN_LEN:,}자 이상 {MODERATE_MAX_LEN:,}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = run_moderate(text)
    except Exception:
        logger.exception("Moderate inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.MODERATE,
        input_text=text,
        output_text=result["highest_label"],
        result_data=result,
    )

    return JsonResponse(result)


@model_login_required
def combo_view(request):
    histories = (
        InferenceHistory.objects
        .filter(user=request.user, task=InferenceHistory.Task.COMBO)
        .order_by("-created_at")[:5]
    )
    return render(request, "my_gpt/combo.html", {"histories": histories})


@model_login_required
def combo_run(request):
    if request.method != "POST":
        return JsonResponse({"error": "허용되지 않은 요청입니다."}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)

    text = body.get("text", "")

    if not isinstance(text, str):
        return JsonResponse({"error": "잘못된 입력값입니다."}, status=400)

    if not text.strip():
        return JsonResponse({"error": "분석할 내용을 입력해주세요."}, status=400)

    if len(text) < COMBO_MIN_LEN:
        return JsonResponse(
            {"error": f"입력값은 {COMBO_MIN_LEN:,}자 이상 입력해주세요."},
            status=400,
        )

    if len(text) > COMBO_MAX_LEN:
        return JsonResponse(
            {"error": f"입력값은 {COMBO_MAX_LEN:,}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = run_combo(text, do_sample=True)
    except Exception:
        logger.exception("Combo inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.COMBO,
        input_text=text,
        output_text=result["summary"],
        result_data=result,
    )

    return JsonResponse(result)