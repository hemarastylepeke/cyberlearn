// Toggle mobile menu
const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');

menuToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
    if (!mobileMenu.classList.contains('hidden')) {
        mobileMenu.style.height = mobileMenu.scrollHeight + "px";
    } else {
        mobileMenu.style.height = "0";
    }
});

// Function to handle commentor clicks
function handleCommentorClick(event) {
  const commentor = event.currentTarget; // Get the clicked commentor
  const commentId = commentor.getAttribute('data-commentor'); // Get the associated comment ID

  // Remove active styles from all commentors
  document.querySelectorAll('[data-commentor]').forEach(c => {
      c.classList.remove('bg-slate-200'); // Remove active background
      c.classList.add('border', 'border-slate-200'); // Add inactive border
  });

  // Add active styles to the clicked commentor
  commentor.classList.add('bg-slate-200'); // Add active background
  commentor.classList.remove('border', 'border-slate-200'); // Remove inactive border

  // Hide all comments
  document.querySelectorAll('.comment').forEach(comment => {
      comment.classList.add('hidden');
  });

  // Show the selected comment
  const selectedComment = document.getElementById(`comment-${commentId}`);
  if (selectedComment) {
      selectedComment.classList.remove('hidden');
  }
}

// Add click event listeners to all commentors
document.querySelectorAll('[data-commentor]').forEach(commentor => {
  commentor.addEventListener('click', handleCommentorClick);
});

// Set the first commentor as active by default
const firstCommentor = document.querySelector('[data-commentor]');
if (firstCommentor) {
  firstCommentor.classList.add('bg-slate-200');
  firstCommentor.classList.remove('border', 'border-slate-200');
}