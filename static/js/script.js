// script.js

let selectedFile = null;

// Drag and drop
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    // Check file type
    if (!['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'].includes(file.type)) {
        showError('Invalid file type. Please use PNG, JPG, JPEG, GIF, or WEBP');
        return;
    }
    
    // Check file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File size too large. Maximum 10MB');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImg').src = e.target.result;
        document.getElementById('imagePreview').style.display = 'block';
        document.getElementById('predictBtn').disabled = false;
        document.getElementById('top3Btn').disabled = false;
        document.getElementById('errorMsg').style.display = 'none';
        document.getElementById('results').style.display = 'none';
        document.getElementById('top3Results').style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function predictImage() {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    showLoading(true);
    document.getElementById('results').style.display = 'none';
    document.getElementById('top3Results').style.display = 'none';
    document.getElementById('errorMsg').style.display = 'none';
    
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Server error'); });
        }
        return response.json();
    })
    .then(data => {
        showLoading(false);
        if (data.status === 'success') {
            displayResult(data);
        } else {
            showError(data.error || 'Prediction failed');
        }
    })
    .catch(error => {
        showLoading(false);
        showError('Error: ' + error.message);
    });
}

function predictTop3() {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    showLoading(true);
    document.getElementById('results').style.display = 'none';
    document.getElementById('top3Results').style.display = 'none';
    document.getElementById('errorMsg').style.display = 'none';
    
    fetch('/predict-top3', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Server error'); });
        }
        return response.json();
    })
    .then(data => {
        showLoading(false);
        if (data.predictions) {
            displayTop3Results(data.predictions);
        } else {
            showError(data.error || 'Prediction failed');
        }
    })
    .catch(error => {
        showLoading(false);
        showError('Error: ' + error.message);
    });
}

function displayResult(data) {
    document.getElementById('resultEmoji').textContent = '🎯';
    document.getElementById('resultObject').textContent = data.object;
    document.getElementById('confidenceFill').style.width = data.confidence + '%';
    document.getElementById('confidenceText').textContent = `Confidence: ${data.confidence}%`;
    document.getElementById('results').style.display = 'block';
}

function displayTop3Results(predictions) {
    let html = '';
    predictions.forEach((pred, idx) => {
        const medalEmoji = ['🥇', '🥈', '🥉'][idx] || '🔹';
        html += `
            <div class="top3-item rank-${pred.rank}">
                <span class="top3-name">${medalEmoji} ${pred.object}</span>
                <span class="top3-confidence">${pred.confidence}%</span>
            </div>
        `;
    });
    
    document.getElementById('top3List').innerHTML = html;
    document.getElementById('results').style.display = 'block';
    document.getElementById('top3Results').style.display = 'block';
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
    document.getElementById('predictBtn').disabled = show;
    document.getElementById('top3Btn').disabled = show;
}

function showError(message) {
    const errorMsg = document.getElementById('errorMsg');
    errorMsg.textContent = message;
    errorMsg.style.display = 'block';
}

function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    document.getElementById('previewImg').src = '';
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('results').style.display = 'none';
    document.getElementById('top3Results').style.display = 'none';
    document.getElementById('errorMsg').style.display = 'none';
    document.getElementById('predictBtn').disabled = true;
    document.getElementById('top3Btn').disabled = true;
}
