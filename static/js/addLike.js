document.addEventListener('DOMContentLoaded', () => {
    const getCSRFToken = () => {
        const csrfForm = document.getElementById('csrf');
        if (csrfForm) {
            const tokenInput = csrfForm.querySelector('input[name="csrfmiddlewaretoken"]');
            return tokenInput ? tokenInput.value : null;
        }
        const hiddenToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return hiddenToken ? hiddenToken.value : null;
    };

    const addLike = async (pk) => {
        const csrfToken = getCSRFToken();
        if (!csrfToken) {
            console.error('CSRF token not found.');
            return;
        }

        console.log(`CSRF Token: ${csrfToken}`);
        console.log(`Post ID: ${pk}`);

        try {
            const response = await fetch('/dorm_guide/add-like/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ pk })
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Success:', data);

                const likeCountElement = document.getElementById(`like-count-${pk}`);
                if (likeCountElement) {
                    likeCountElement.textContent = parseInt(likeCountElement.textContent) + 1;
                }
            } else {
                console.error('Failed to add like:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    window.addLike = addLike;
});
