// Toggle language dropdown
document.addEventListener('DOMContentLoaded', function() {
  const langButton = document.querySelector('.language-dropdown-button');
  const langMenu = document.querySelector('.language-dropdown-menu');
  
  if (langButton && langMenu) {
    langButton.addEventListener('click', function() {
      langMenu.classList.toggle('hidden');
    });
    
    // Close the dropdown when clicking outside
    document.addEventListener('click', function(event) {
      if (!langButton.contains(event.target) && !langMenu.contains(event.target)) {
        langMenu.classList.add('hidden');
      }
    });
  }
});
