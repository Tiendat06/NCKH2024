document.getElementById('toggleButton').addEventListener('click', function() {
    const specificSidebar = document.getElementById('specificSidebar');
    const content = document.querySelector('.content');
  
    specificSidebar.classList.toggle('collapsed');
    content.classList.toggle('collapsed');
  });
  