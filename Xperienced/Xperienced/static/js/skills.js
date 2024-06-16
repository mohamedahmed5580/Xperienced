document.addEventListener('DOMContentLoaded', (event) => {
    const skillsInput = document.getElementById('skill-input');
    const skillsList = document.getElementById('skills-list');
    const addSkillButton = document.getElementById('add-skill-button');
    const removeSkillButtons = document.getElementsByClassName('remove-skill-button');

    const loadSkills = () => {
        const skills = JSON.parse(localStorage.getItem('skills')) || [];
        skillsList.innerHTML = '';
        skills.forEach(skill => {
            const li = document.createElement('li');
            li.className = 'skill';
            li.innerHTML = `
                <i class="fa fa-fw fa-tag"></i><bdi>${skill}</bdi>
                <button type="button" class="btn btn-danger remove-skill-button" data-skill="${skill}">Remove</button>
            `;
            skillsList.appendChild(li);
        });

        // Attach event listeners to remove buttons
        Array.from(removeSkillButtons).forEach(button => {
            button.addEventListener('click', removeSkill);
        });
    };

    const addSkill = () => {
        const skill = skillsInput.value.trim();
        if (skill) {
            const skills = JSON.parse(localStorage.getItem('skills')) || [];
            skills.push(skill);
            localStorage.setItem('skills', JSON.stringify(skills));
            skillsInput.value = '';

            const formData = {
                'skill-input': skill,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
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

    const removeSkill = (event) => {
        const skillToRemove = event.target.getAttribute('data-skill');
        if (skillToRemove) {
            const formData = {
                'skill-name': skillToRemove,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            };

            $.ajax({
                type: 'DELETE',
                url: '/profile/skills',
                data: JSON.stringify(formData),
                success: function(response) {
                    if (response.status === 'success') {
                        // Remove skill from local storage
                        let skills = JSON.parse(localStorage.getItem('skills')) || [];
                        skills = skills.filter(skill => skill !== skillToRemove);
                        localStorage.setItem('skills', JSON.stringify(skills));

                        // Reload the page to show the updated skills list
                        location.reload();
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
    loadSkills();
});
