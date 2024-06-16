document.addEventListener('DOMContentLoaded', (event) => {
  const skillsInput = document.getElementById('skill-input');
  const skillsList = document.getElementById('skills-list');
  const addSkillButton = document.getElementById('add-skill-button');

  // Load skills from local storage and display them
  const loadSkills = () => {
      const skills = JSON.parse(localStorage.getItem('skills')) || [];
      skillsList.innerHTML = '';
      skills.forEach(skill => {
          const li = document.createElement('li');
          li.className = 'skill';
          li.innerHTML = `<i class="fa fa-fw fa-tag"></i><bdi>${skill}</bdi>`;
          skillsList.appendChild(li);
      });
  };

  // Add skill to local storage and make an AJAX request
  const addSkill = () => {
      const skill = skillsInput.value.trim();
      if (skill) {
          const skills = JSON.parse(localStorage.getItem('skills')) || [];
          skills.push(skill);
          localStorage.setItem('skills', JSON.stringify(skills));
          skillsInput.value = '';
        //   loadSkills();

          // Make AJAX request to send the skill to the server
          const formData = {
              'skill-input': skill,
              'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
          };

          $.ajax({
              type: 'POST',
              url: 'skills', // Change this to your actual URL
              data: formData,
              success: function(response) {
                  console.log('Data sent successfully.');
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


$('#skills-form').on('submit', function(event) {
    var formData = {
      'skill-input': $('#skill-input').val(),
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    };

    $.ajax({
        type: 'POST',
        url: 'skills', // Change this to your actual signup URL
        data: {'skill-input': $('#skill-input').val(),},
        success: function(response) {
            console.log('Data sent successfully.');
        },
        error: function(error) {
            console.log('An error occurred.');
            console.log(error);
        }
    });
});