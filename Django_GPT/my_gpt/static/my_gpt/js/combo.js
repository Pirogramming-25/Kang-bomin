document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("combo-input");
    const btn = document.getElementById("combo-btn");
    const regenBtn = document.getElementById("combo-regenerate-btn");
    const loading = document.getElementById("combo-loading");
    const errorBox = document.getElementById("combo-error");
    const resultBox = document.getElementById("combo-result");

    let lastText = "";

    async function runCombo(text) {
        errorBox.textContent = "";
        btn.disabled = true;
        regenBtn.disabled = true;
        input.disabled = true;
        loading.style.display = "block";

        try {
            const response = await fetch("/combo/run/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ text }),
            });

            const data = await response.json();

            if (!response.ok) {
                errorBox.textContent = data.error || "오류가 발생했습니다.";
                return;
            }

            const allScoresHtml = data.toxicity.all_scores
                .map(s => `<li>${s.label}: ${(s.score * 100).toFixed(2)}%</li>`)
                .join("");

            resultBox.innerHTML = `
                <h3>입력 원문</h3>
                <p>${text}</p>

                <h3>요약문</h3>
                <p>${data.summary}</p>

                <h3>감정 분석</h3>
                <p>${data.sentiment.label} (${(data.sentiment.score * 100).toFixed(2)}%)</p>

                <h3>유해 표현 분석</h3>
                <p>최고 위험: ${data.toxicity.highest_label} (${(data.toxicity.highest_score * 100).toFixed(2)}%)</p>
                <ul>${allScoresHtml}</ul>

                <h3>종합 판정</h3>
                <p>${data.verdict}</p>
            `;

            lastText = text;
            regenBtn.style.display = "inline-block";
        } catch (err) {
            errorBox.textContent = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.";
        } finally {
            btn.disabled = false;
            regenBtn.disabled = false;
            input.disabled = false;
            loading.style.display = "none";
        }
    }

    btn.addEventListener("click", () => {
        runCombo(input.value);
    });

    regenBtn.addEventListener("click", () => {
        if (lastText) {
            runCombo(lastText);
        }
    });
});