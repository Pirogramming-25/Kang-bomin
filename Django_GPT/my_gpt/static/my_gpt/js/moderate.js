document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("moderate-input");
    const btn = document.getElementById("moderate-btn");
    const loading = document.getElementById("moderate-loading");
    const errorBox = document.getElementById("moderate-error");
    const resultBox = document.getElementById("moderate-result");

    btn.addEventListener("click", async () => {
        const text = input.value;

        errorBox.textContent = "";
        resultBox.textContent = "";
        btn.disabled = true;
        input.disabled = true;
        loading.style.display = "block";

        try {
            const response = await fetch("/moderate/run/", {
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

            const allScoresHtml = data.all_scores
                .map(s => `<li>${s.label}: ${(s.score * 100).toFixed(2)}%</li>`)
                .join("");

            resultBox.innerHTML = `
                <p>최고 위험 레이블: ${data.highest_label}</p>
                <p>위험 점수: ${(data.highest_score * 100).toFixed(2)}%</p>
                <ul>${allScoresHtml}</ul>
            `;
        } catch (err) {
            errorBox.textContent = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.";
        } finally {
            btn.disabled = false;
            input.disabled = false;
            loading.style.display = "none";
        }
    });
});