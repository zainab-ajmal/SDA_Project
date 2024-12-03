const bookList = document.getElementById('book-list');

// Function to update the list of all books
function updateBookList() {
    fetch('/upload/', { method: 'GET' }) // Fetch all books
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            bookList.innerHTML = ''; // Clear the current book list
            if (data.length === 0) {
                bookList.innerHTML = '<p>No books found. Please upload a book.</p>';
            } else {
                data.forEach((pdf) => {
                    const listItem = document.createElement('li');
                    listItem.classList.add('book-item'); // Add a class for styling
                    listItem.innerHTML = `
                        <strong>${pdf.name}</strong>
                        <p>${pdf.description}</p>
                        <a href="${pdf.file}" target="_blank" class="download-link">Download</a>
                    `;
                    bookList.appendChild(listItem);
                });
            }
        })
        .catch((error) => {
            console.error('Error fetching book list:', error);
            bookList.innerHTML = '<p>Error loading books. Please try again later.</p>';
        });
}

// Initialize the book list
updateBookList();
