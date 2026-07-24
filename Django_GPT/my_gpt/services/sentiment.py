from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device

MODEL_ID = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    return pipeline(
        task="text-classification",
        model=MODEL_ID,
        top_k=None,
        device=get_pipeline_device(),
    )


def run_sentiment(text: str) -> dict:
    classifier = get_sentiment_pipeline()
    results = classifier(text)[0]

    # results: [{"label": "positive", "score": 0.92}, ...]
    sorted_results = sorted(
        results, key=lambda x: x["score"], reverse=True
    )
    top = sorted_results[0]

    return {
        "label": top["label"],
        "score": top["score"],
        "all_scores": sorted_results,
    }