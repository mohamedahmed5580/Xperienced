document.addEventListener('DOMContentLoaded', (event) => {
    const skillsInput = document.getElementById('skill-input');
    const skillsList = document.getElementById('skills-list');
    const addSkillButton = document.getElementById('add-skill-button');
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    const setupCSRFToken = () => {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", csrfToken);
                }
            }
        });
    };

    setupCSRFToken();
    // Add CSRF token to AJAX requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    const addSkill = () => {
        const skill = skillsInput.value.trim();
        if (skill) {
            const skills = JSON.parse(localStorage.getItem('skills')) || [];
            skills.push(skill);
            localStorage.setItem('skills', JSON.stringify(skills));
            skillsInput.value = '';

            const formData = {
                'skill-input': skill,
                'csrfmiddlewaretoken': csrftoken
            };

            $.ajax({
                type: 'POST',
                url: '/profile/skills',
                data: formData,
                success: function(response) {
                    if (response.status === 'success') {
                        location.reload(); // Reload the page to show the updated skills list
                    }
                },
                error: function(error) {
                    console.log('An error occurred.');
                    console.log(error);
                }
            });
        }
    };

    addSkillButton.addEventListener('click', addSkill);
});
