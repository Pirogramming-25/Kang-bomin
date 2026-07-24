from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device

MODEL_ID = "sshleifer/distilbart-cnn-6-6"


@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    return pipeline(
        task="summarization",
        model=MODEL_ID,
        device=get_pipeline_device(),
    )


def run_summarize(text: str, do_sample: bool = False) -> dict:
    summarizer = get_summarizer_pipeline()

    input_word_count = len(text.split())
    max_len = max(20, min(180, int(input_word_count * 0.6)))
    min_len = max(10, int(max_len * 0.3))

    kwargs = {"max_length": max_len, "min_length": min_len}
    if do_sample:
        kwargs.update(
            do_sample=True,
            top_p=0.9,
            temperature=0.8,
        )

    result = summarizer(text, **kwargs)[0]
    summary = result["summary_text"]

    original_len = len(text)
    summary_len = len(summary)
    ratio = (summary_len / original_len) * 100 if original_len else 0

    return {
        "summary": summary,
        "original_length": original_len,
        "summary_length": summary_len,
        "summary_ratio": round(ratio, 2),
    }