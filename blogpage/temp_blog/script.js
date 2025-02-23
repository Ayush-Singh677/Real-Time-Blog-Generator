// Handle "Read More" button toggle
document.querySelectorAll('.read-more-btn').forEach(button => {
    button.addEventListener('click', function () {
      const commentsSection = this.nextElementSibling;
      commentsSection.style.display = commentsSection.style.display === 'block' ? 'none' : 'block';
    });
  });
  
  document.querySelectorAll('.comment-form').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const commentText = this.querySelector('textarea').value.trim();
      if (commentText) {
        const newComment = document.createElement('div');
        newComment.classList.add('comment');
        newComment.innerHTML = `<p><strong>You:</strong> ${commentText}</p>`;
        this.parentNode.insertBefore(newComment, this);
        this.reset();
      }
    });
  });
  
  document.querySelectorAll('.like-btn').forEach(button => {
    let liked = false;
    let count = 0;
  
    button.addEventListener('click', function () {
      const likeCountElement = this.querySelector('.like-count');
  
      if (!liked) {
        count++;
        liked = true;
        this.style.backgroundColor = '#ffe6e6';
        this.style.borderColor = '#ffcccc';
      } else {
        count--;
        liked = false;
        this.style.backgroundColor = '#fff';
        this.style.borderColor = '#ddd';
      }
  
      likeCountElement.textContent = count;
    });
  });