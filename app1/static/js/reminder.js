document.getElementById('reminderForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    const reminderDateTime = new Date(`${date}T${time}`);
    const currentTime = new Date();

    if (reminderDateTime <= currentTime) {
        alert('Please set a future date and time.');
        return;
    }

    addReminderToTable(title, description, reminderDateTime);
    scheduleNotification(title, description, reminderDateTime);
});

function addReminderToTable(title, description, dateTime) {
    const tableBody = document.getElementById('reminderTable');
    const row = document.createElement('tr');

    row.innerHTML = `
    <td>${title}</td>
    <td>${description}</td>
    <td>${dateTime.toLocaleString()}</td>
    <td><button class="delete-button">Delete</button></td>
  `;

    tableBody.appendChild(row);

    row.querySelector('.delete-button').addEventListener('click', () => {
        row.remove();
    });
}

function scheduleNotification(title, description, dateTime) {
    const delay = dateTime - new Date();

    if (delay > 0) {
        setTimeout(() => {
            showNotification(title, description);
        }, delay);
    } else {
        alert("The scheduled time has already passed.");
    }
}

function showNotification(title, description) {
    if (Notification.permission === 'granted') {
        new Notification(title, {
            body: description,
            icon: 'https://via.placeholder.com/48' // Placeholder for notification icon
        });
          // Add points after a successful reminder addition
  userPoints += 5; // Increment points
  updatePointsOnHomePage(); // Update points display
  console.log(`Points after adding a reminder: ${userPoints}`);
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                new Notification(title, {
                    body: description,
                    icon: 'https://via.placeholder.com/48'
                });
            }
        });
    } else {
        alert('You have blocked notifications. Please enable them in your browser settings.');
    }
}

// Request notification permission on page load
if (Notification.permission === 'default') {
    Notification.requestPermission();
}
