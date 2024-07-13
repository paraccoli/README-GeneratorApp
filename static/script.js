document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('readme-form');
    const resultDiv = document.getElementById('result');
    const readmeContent = document.getElementById('readme-content');
    const previewDiv = document.getElementById('preview');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const projectName = document.getElementById('project-name').value;
        const projectDescription = document.getElementById('project-description').value;
        const projectFeatures = document.getElementById('project-features').value;

        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                projectName,
                projectDescription,
                projectFeatures,
            }),
        })
        .then(response => response.json())
        .then(data => {
            readmeContent.textContent = data.readme;
            resultDiv.style.display = 'block';
            renderMarkdown(data.readme);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the README.');
        });
    });

    function renderMarkdown(markdown) {
        fetch('/render_markdown', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ markdown: markdown }),
        })
        .then(response => response.text())
        .then(html => {
            previewDiv.innerHTML = html;
            previewDiv.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while rendering the markdown.');
        });
    }
});
