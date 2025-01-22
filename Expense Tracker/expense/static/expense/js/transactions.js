// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function () {
  // Get the input field for new category
  const inputField = document.getElementById("addNewCategory");

  // Add event listener for 'Enter' key press
  inputField.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      // Check if Enter key was pressed
      // Find the form
      const form = inputField.closest("form");

      // Optionally, you can validate or perform other checks here before submitting
      form.submit(); // Submit the form
    }
  });
});
