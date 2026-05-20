document.addEventListener('DOMContentLoaded', function() {
    let sessionId = generateSessionId();
    let isLoading = false;
    let messages = [];

    const resumeStage = document.getElementById('resumeStage');
    const interviewStage = document.getElementById('interviewStage');
    const completeStage = document.getElementById('completeStage');
    const resumeInput = document.getElementById('resumeInput');
    const startBtn = document.getElementById('startBtn');
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');
    const messagesContainer = document.getElementById('messagesContainer');
    const restartBtn = document.getElementById('restartBtn');
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const step3 = document.getElementById('step3');

    function generateSessionId() {
        return 'interview_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    startBtn.addEventListener('click', function() {
        const resume = resumeInput.value.trim();
        if (!resume) {
            alert('请输入您的简历内容');
            return;
        }

        startInterview(resume);
    });

    sendBtn.addEventListener('click', function() {
        sendMessage();
    });

    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    restartBtn.addEventListener('click', function() {
        sessionId = generateSessionId();
        messages = [];
        resumeInput.value = '';
        messagesContainer.innerHTML = '';
        showStage('resume');
    });

    async function startInterview(resume) {
        showStage('interview');
        step1.classList.add('completed');
        step2.classList.add('active');

        const systemMessage = `用户简历：\n${resume}\n\n请开始面试。`;
        await sendToAI(systemMessage);
    }

    async function sendMessage() {
        if (isLoading) return;

        const text = userInput.value.trim();
        if (!text) return;

        userInput.value = '';
        addMessage(text, 'user');
        await sendToAI(text);
    }

    async function sendToAI(text) {
        isLoading = true;
        sendBtn.classList.add('loading');
        sendBtn.disabled = true;

        const aiMessageEl = createEmptyAIMessage();
        let fullResponse = '';

        try {
            const response = await fetch('/api/interview/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    sessionId: sessionId,
                    message: text
                }),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.substring(6);
                        if (data === '[DONE]') {
                            continue;
                        }

                        try {
                            const json = JSON.parse(data);
                            if (json.content) {
                                fullResponse += json.content;
                                updateAIMessage(aiMessageEl, fullResponse);
                            }
                        } catch (e) {
                            // 忽略解析错误
                        }
                    }
                }
            }

            if (fullResponse) {
                messages.push({ role: 'assistant', content: fullResponse });
            }

        } catch (error) {
            console.error('Error:', error);
            addMessage('抱歉，发生了错误，请重试。', 'ai');
        }

        isLoading = false;
        sendBtn.classList.remove('loading');
        sendBtn.disabled = false;
        userInput.focus();
    }

    function createEmptyAIMessage() {
        const messageEl = document.createElement('div');
        messageEl.className = 'message message-ai';
        messageEl.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <span class="typing-text"></span>
            </div>
        `;
        messagesContainer.appendChild(messageEl);
        scrollToBottom();
        return messageEl;
    }

    function updateAIMessage(el, content) {
        const textEl = el.querySelector('.typing-text');
        let processedContent = content;

        const timePattern = /\[⏱️\s*(\d+)分钟\]/g;
        const matches = [...content.matchAll(timePattern)];

        if (matches.length > 0) {
            processedContent = content.replace(timePattern, '');
        }

        textEl.textContent = processedContent;

        if (matches.length > 0 && !el.querySelector('.time-estimate')) {
            const timeEstimate = matches[matches.length - 1][0];
            const contentEl = el.querySelector('.message-content');
            const timeEl = document.createElement('div');
            timeEl.className = 'time-estimate';
            timeEl.textContent = timeEstimate;
            contentEl.appendChild(timeEl);
        }

        scrollToBottom();
    }

    function addMessage(text, role) {
        const messageEl = document.createElement('div');
        messageEl.className = `message message-${role}`;

        if (role === 'user') {
            messageEl.innerHTML = `
                <div class="message-content">${escapeHtml(text)}</div>
                <div class="message-avatar">👤</div>
            `;
        } else {
            messageEl.innerHTML = `
                <div class="message-avatar">🤖</div>
                <div class="message-content">${escapeHtml(text)}</div>
            `;
        }

        messagesContainer.appendChild(messageEl);
        messages.push({ role, content: text });
        scrollToBottom();
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function showStage(stage) {
        resumeStage.style.display = 'none';
        interviewStage.style.display = 'none';
        completeStage.style.display = 'none';

        step1.classList.remove('active', 'completed');
        step2.classList.remove('active', 'completed');
        step3.classList.remove('active', 'completed');

        if (stage === 'resume') {
            resumeStage.style.display = 'flex';
            step1.classList.add('active');
        } else if (stage === 'interview') {
            interviewStage.style.display = 'flex';
            step1.classList.add('completed');
            step2.classList.add('active');
        } else if (stage === 'complete') {
            completeStage.style.display = 'flex';
            step1.classList.add('completed');
            step2.classList.add('completed');
            step3.classList.add('active');
        }
    }

    showStage('resume');
});
