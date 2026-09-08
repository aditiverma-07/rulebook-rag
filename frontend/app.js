document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('ask-form');
    const input = document.getElementById('query-input');
    const submitBtn = document.getElementById('submit-btn');
    const exampleBtns = document.querySelectorAll('.example-btn');
    
    const loadingState = document.getElementById('loading-state');
    const loadingText = document.getElementById('loading-text');
    
    const resultArea = document.getElementById('result-area');
    const statusBanner = document.getElementById('status-banner');
    const answerContainer = document.getElementById('answer-container');
    const answerText = document.getElementById('answer-text');
    const evidenceContainer = document.getElementById('evidence-container');
    const evidenceList = document.getElementById('evidence-list');
    const evidenceTitle = document.getElementById('evidence-title');
    const errorContainer = document.getElementById('error-container');
    const errorText = document.getElementById('error-text');

    // Populate input when example is clicked
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            input.value = e.target.textContent;
            input.focus();
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const query = input.value.trim();
        if (!query) return;

        // Reset UI
        submitBtn.disabled = true;
        resultArea.classList.add('hidden');
        resultArea.classList.remove('state-answered', 'state-conflict', 'state-not-covered');
        errorContainer.classList.add('hidden');
        answerContainer.classList.add('hidden');
        evidenceContainer.classList.add('hidden');
        evidenceList.innerHTML = '';
        
        // Show Loading
        loadingState.classList.remove('hidden');
        loadingText.textContent = "Searching and evaluating the rulebook...";

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });

            if (!response.ok) {
                let errDetail = `HTTP ${response.status}`;
                try {
                    const errData = await response.json();
                    if (errData.detail) {
                        errDetail = errData.detail;
                    }
                } catch (e) {}
                throw new Error(`Unable to reach the rulebook service. (${errDetail})`);
            }

            const data = await response.json();
            renderResult(data);

        } catch (error) {
            resultArea.classList.remove('hidden');
            errorContainer.classList.remove('hidden');
            errorText.textContent = error.message || "A network error occurred. Please make sure the FastAPI server is running.";
        } finally {
            loadingState.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    function renderResult(data) {
        resultArea.classList.remove('hidden');
        
        const type = data.type; // "answered", "conflict", "not_covered"
        
        // Handle Banner
        if (type === "answered") {
            resultArea.classList.add('state-answered');
            statusBanner.textContent = "Answered";
        } else if (type === "conflict") {
            resultArea.classList.add('state-conflict');
            statusBanner.innerHTML = "⚠ Conflicting Provisions Found";
        } else if (type === "not_covered") {
            resultArea.classList.add('state-not-covered');
            statusBanner.textContent = "Not Covered";
        }

        // Handle Answer text
        if (type === "answered" || type === "conflict" || type === "not_covered") {
            answerContainer.classList.remove('hidden');
            answerText.textContent = data.answer;
        }

        // Handle Evidence
        if (data.evidence && data.evidence.length > 0) {
            evidenceContainer.classList.remove('hidden');
            
            if (type === "not_covered") {
                evidenceTitle.textContent = "Related retrieved material";
            } else {
                evidenceTitle.textContent = "Supporting Evidence";
            }

            data.evidence.forEach((item, index) => {
                const card = document.createElement('div');
                card.className = 'evidence-card';

                const similarityPct = (item.similarity * 100).toFixed(1);

                let metaHTML = `
                    <div class="evidence-meta">
                        <div class="meta-item">
                            <strong>Source:</strong> ${item.source}
                        </div>
                `;
                if (item.section) {
                    metaHTML += `
                        <div class="meta-item">
                            <strong>Section:</strong> ${item.section}
                        </div>
                    `;
                }
                if (item.page !== null && item.page !== undefined) {
                    metaHTML += `
                        <div class="meta-item">
                            <strong>Page:</strong> ${item.page}
                        </div>
                    `;
                }
                metaHTML += `
                        <div class="meta-item">
                            <strong>Similarity:</strong> <span class="similarity-badge">${similarityPct}%</span>
                        </div>
                    </div>
                `;

                card.innerHTML = `
                    ${metaHTML}
                    <div class="evidence-text">${item.text}</div>
                `;

                evidenceList.appendChild(card);
            });
        }
    }
});
