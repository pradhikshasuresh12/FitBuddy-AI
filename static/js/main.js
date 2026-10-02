/* main.js — FitBuddy frontend interactions */

document.addEventListener("DOMContentLoaded", function () {
    // ---- Form submit: show loading state ----
    const planForm = document.getElementById("planForm");
    if (planForm) {
        planForm.addEventListener("submit", function () {
            const btn = document.getElementById("generateBtn");
            const btnText = btn.querySelector(".btn-text");
            const btnLoader = btn.querySelector(".btn-loader");
            btn.disabled = true;
            btnText.hidden = true;
            btnLoader.hidden = false;
        });
    }

    // ---- Result page: render Markdown plan ----
    const planContent = document.getElementById("planContent");
    const planRender = document.getElementById("planRender");
    if (planContent && planRender) {
        const rawPlan = planContent.textContent.trim();
        if (typeof marked !== "undefined") {
            planRender.innerHTML = marked.parse(rawPlan);
        } else {
            planRender.innerHTML = "<pre>" + rawPlan + "</pre>";
        }
    }
});
