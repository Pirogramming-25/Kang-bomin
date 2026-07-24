document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("sentiment-input");
    const btn = document.getElementById("sentiment-btn");
    const loading = document.getElementById("sentiment-loading");
    const errorBox = document.getElementById("sentiment-error");
    const resultBox = document.getElementById("sentiment-result");
    const historyBox = document.getElementById("sentiment-history");

    const isLoggedIn = historyBox.dataset.loggedIn === "true";
    let guestHistory = [];

    function renderGuestHistory() {
        if (guestHistory.length === 0) {
            historyBox.innerHTML = "<li>기록이 없습니다.</li>";
            return;
        }
        historyBox.innerHTML = guestHistory
            .map(h => `<li>${h.text.slice(0, 30)} → ${h.label} (${(h.score * 100).toFixed(2)}%)</li>`)
            .join("");
    }

    btn.addEventListener("click", async () => {
        const text = input.value;

        errorBox.textContent = "";
        resultBox.textContent = "";
        btn.disabled = true;
        input.disabled = true;
        loading.style.display = "block";

        try {
            const response = await fetch("/sentiment/run/", {
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
                <p>감정: ${data.label}</p>
                <p>신뢰도: ${(data.score * 100).toFixed(2)}%</p>
            `;

            if (!isLoggedIn) {
                guestHistory.unshift({ text, label: data.label, score: data.score });
                guestHistory = guestHistory.slice(0, 5);
                renderGuestHistory();
            }
        } catch (err) {
            errorBox.textContent = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.";
        } finally {
            btn.disabled = false;
            input.disabled = false;
            loading.style.display = "none";
        }
    });
});