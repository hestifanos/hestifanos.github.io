// Wait for the DOM content to be fully loaded before executing JavaScript
document.addEventListener("DOMContentLoaded", function () {
  // Get a reference to the contact form
  var contactForm = document.getElementById("contact-form");

  // Add an event listener to the form submission
  contactForm.addEventListener("submit", function (event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the values entered by the user in the form fields
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var message = document.getElementById("message").value;

    // Send an AJAX request to submit the form data to the server
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/submit_contact_form", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Define the data to be sent in JSON format
    var formData = JSON.stringify({
      name: name,
      email: email,
      message: message,
    });

    // Define the callback function to handle the server response
    xhr.onload = function () {
      if (xhr.status === 200) {
        // Handle successful form submission (if needed)
        console.log("Form submitted successfully!");
      } else {
        // Handle errors or validation failures (if needed)
        console.error("Error submitting form:", xhr.statusText);
      }
    };

    // Send the AJAX request with the form data
    xhr.send(formData);
  });
});
