document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateBtn');
    const createNewBtn = document.getElementById('createNewBtn');
    const formSection = document.getElementById('formSection');
    const resultSection = document.getElementById('resultSection');
    
    const petType = document.getElementById('petType');
    const petName = document.getElementById('petName');
    const petFeatures = document.getElementById('petFeatures');

    generateBtn.addEventListener('click', async function() {
        if (!validateForm()) {
            return;
        }

        generateBtn.classList.add('loading');
        generateBtn.disabled = true;

        try {
            const response = await fetch('/api/pet-coin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    petType: petType.value,
                    petName: petName.value,
                    petFeatures: petFeatures.value
                }),
            });

            const data = await response.json();

            if (data.status === 'success') {
                displayResult(data);
                formSection.style.display = 'none';
                resultSection.style.display = 'block';
            } else {
                alert('生成失败，请稍后重试');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('网络错误，请检查网络连接');
        } finally {
            generateBtn.classList.remove('loading');
            generateBtn.disabled = false;
        }
    });

    createNewBtn.addEventListener('click', function() {
        resultSection.style.display = 'none';
        formSection.style.display = 'block';
        petName.value = '';
        petFeatures.value = '';
        petType.value = '';
    });

    function validateForm() {
        if (!petType.value) {
            alert('请选择宠物类型');
            petType.focus();
            return false;
        }
        if (!petName.value.trim()) {
            alert('请输入宠物名字');
            petName.focus();
            return false;
        }
        if (!petFeatures.value.trim()) {
            alert('请描述宠物特点');
            petFeatures.focus();
            return false;
        }
        return true;
    }

    function displayResult(data) {
        document.getElementById('coinTitle').textContent = data.coinTitle || '冥币';
        document.getElementById('coinIcon').textContent = data.coinIcon || '🐾';
        document.getElementById('coinValue').textContent = data.coinValue || '100万';
        document.getElementById('coinName').textContent = data.coinName || '';
        document.getElementById('coinDesc').textContent = data.coinDesc || '';
        document.getElementById('resultPetName').textContent = data.petName || '';
        document.getElementById('resultPetType').textContent = data.petTypeName || '';
        document.getElementById('resultCoinValue').textContent = data.coinValue || '100万冥币';
    }
});
