// Function to get and display the current date and time
function updateDateTime() {
	const now = new Date();
	const date = now.toLocaleDateString(); // Get the date in the user's local format
	const time = now.toLocaleTimeString(); // Get the time in the user's local format

	// Combine date and time into one string
	const dateTimeString = `Date: ${date} | Time: ${time}`;

	// Display the date and time in the element
	document.getElementById("datetime").innerText = dateTimeString;
}

// Update the date and time every second
setInterval(updateDateTime, 1000);

// Call the function initially to avoid delay
updateDateTime();
