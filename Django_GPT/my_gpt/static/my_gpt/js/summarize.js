document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("summarize-input");
    const btn = document.getElementById("summarize-btn");
    const loading = document.getElementById("summarize-loading");
    const errorBox = document.getElementById("summarize-error");
    const resultBox = document.getElementById("summarize-result");

    btn.addEventListener("click", async () => {
        const text = input.value;

        errorBox.textContent = "";
        resultBox.textContent = "";
        btn.disabled = true;
        input.disabled = true;
        loading.style.display = "block";

        try {
            const response = await fetch("/summarize/run/", {
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

            resultBox.innerHTML = `
                <p>원문 길이: ${data.original_length}자</p>
                <p>요약문 길이: ${data.summary_length}자</p>
                <p>요약 비율: ${data.summary_ratio}%</p>
                <p><strong>요약 결과:</strong></p>
                <p>${data.summary}</p>
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