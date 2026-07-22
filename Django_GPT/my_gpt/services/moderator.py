from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device

MODEL_ID = "unitary/toxic-bert"


@lru_cache(maxsize=1)
def get_moderator_pipeline():
    return pipeline(
        task="text-classification",
        model=MODEL_ID,
        top_k=None,
        device=get_pipeline_device(),
    )


def run_moderate(text: str) -> dict:
    moderator = get_moderator_pipeline()
    results = moderator(text)[0]

    sorted_results = sorted(
        results, key=lambda x: x["score"], reverse=True
    )
    top = sorted_results[0]

    return {
        "highest_label": top["label"],
        "highest_score": top["score"],
        "all_scores": sorted_results,
    }