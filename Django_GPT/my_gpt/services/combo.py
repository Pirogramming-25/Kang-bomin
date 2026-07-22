from .summarizer import run_summarize
from .sentiment import run_sentiment
from .moderator import run_moderate


def run_combo(text: str, do_sample: bool = True) -> dict:
    summary_result = run_summarize(text, do_sample=do_sample)
    summary_text = summary_result["summary"]

    sentiment_result = run_sentiment(summary_text)
    toxicity_result = run_moderate(summary_text)

    sentiment_desc = (
        "부정적인 평가를 포함합니다."
        if sentiment_result["label"].lower() == "negative"
        else "강한 부정적 평가는 확인되지 않았습니다."
    )

    toxicity_desc = (
        "유해 표현 가능성이 높습니다."
        if toxicity_result["highest_score"] >= 0.5
        else "심각한 유해 표현 가능성은 낮습니다."
    )

    verdict = f"{sentiment_desc} {toxicity_desc}"

    return {
        "summary": summary_text,
        "sentiment": {
            "label": sentiment_result["label"],
            "score": sentiment_result["score"],
        },
        "toxicity": {
            "highest_label": toxicity_result["highest_label"],
            "highest_score": toxicity_result["highest_score"],
            "all_scores": toxicity_result["all_scores"],
        },
        "verdict": verdict,
    }