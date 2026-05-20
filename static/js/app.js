document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.getElementById('submitBtn');
    const userInput = document.getElementById('userInput');
    const outputArea = document.getElementById('outputArea');

    if (submitBtn && userInput && outputArea) {
        submitBtn.addEventListener('click', async function() {
            const input = userInput.value.trim();
            if (!input) {
                outputArea.innerHTML = '<p style="color: #ff6b6b; text-align: center;">请输入内容后再提交</p>';
                return;
            }

            submitBtn.disabled = true;
            submitBtn.textContent = '处理中...';
            outputArea.innerHTML = '<p style="text-align: center; color: #86868b;">正在处理，请稍候...</p>';

            try {
                const response = await fetch(`/api/${currentAppId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ input: input }),
                });

                const data = await response.json();

                if (data.status === 'success') {
                    outputArea.innerHTML = `
                        <div style="margin-bottom: 16px;">
                            <strong style="color: #667eea;">✓ 请求成功</strong>
                        </div>
                        <div style="background: #fff; padding: 16px; border-radius: 8px; margin-bottom: 12px;">
                            <strong>输入内容：</strong>
                            <p style="margin-top: 8px; color: #6e6e73;">${data.input}</p>
                        </div>
                        <div style="background: #fff; padding: 16px; border-radius: 8px;">
                            <strong>输出结果：</strong>
                            <p style="margin-top: 8px; color: #1d1d1f;">${data.output}</p>
                        </div>
                    `;
                } else {
                    outputArea.innerHTML = '<p style="color: #ff6b6b;">请求失败，请稍后重试</p>';
                }
            } catch (error) {
                console.error('Error:', error);
                outputArea.innerHTML = '<p style="color: #ff6b6b;">网络错误，请稍后重试</p>';
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = '提交';
            }
        });
    }
});
