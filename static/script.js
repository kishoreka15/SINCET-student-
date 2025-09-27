// Login form submit
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const feedback = document.getElementById('feedback');
        if (data.status === 'success') {
            feedback.textContent = 'Login successful! Redirecting...';
            feedback.className = 'success';
            setTimeout(() => window.location.href = '/', 1000);  // Redirect to tasks
        } else {
            feedback.textContent = data.message;
            feedback.className = 'error';
        }
    })
    .catch(error => {
        document.getElementById('feedback').textContent = 'Error: ' + error;
    });
});

// Previous task JS remains (loadTasks, etc.)
function loadTasks() { /* ... as before */ }
// ... rest unchanged