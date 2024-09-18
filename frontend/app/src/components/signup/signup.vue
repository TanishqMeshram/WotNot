<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-white p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl sm:text-3xl font-semibold text-center text-gray-800 mb-4">Get started with Wotnot</h2>

      <hr class="my-3 border-gray-300" />

      <div class="space-y-4">
        <div class="w-full">
          <label for="username" class="block text-sm font-medium text-gray-700">Business Name</label>
          <input type="text" id="username" placeholder="Your Business Name" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" required />
        </div>

        <div class="w-full">
          <label for="email" class="block text-sm font-medium text-gray-700">Business Email Address</label>
          <input type="email" id="email" placeholder="Your Business Email Address" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" required />
        </div>

        <div class="w-full">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" id="password" placeholder="Set Password" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" required />
        </div>

        <div class="w-full">
          <label for="WABAID" class="block text-sm font-medium text-gray-700">WhatsApp Business Account ID</label>
          <input type="text" id="WABAID" placeholder="Your WhatsApp Business Account ID" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" required />
        </div>

        <div class="w-full">
          <label for="PAccessToken" class="block text-sm font-medium text-gray-700">Permanent Access Token</label>
          <input type="text" id="PAccessToken" placeholder="Your Permanent Access Token" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" required />
        </div>

        <div class="w-full">
          <label for="Phone_id" class="block text-sm font-medium text-gray-700">Phone Number ID</label>
          <input type="text" id="Phone_id" placeholder="Your Phone Number ID" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" required />
        </div>
      </div>

      <div class="mt-4 text-sm text-center">
        <p class="mb-2 text-sm">
          By signing up you agree to the
          <a href="#" class="text-[#075e54] font-semibold">Terms</a> and
          <a href="#" class="text-[#075e54] font-semibold">Privacy Policy</a>
        </p>
      </div>

      <button class="w-full bg-[#075e54] text-white py-2 rounded-md hover:bg-[#2d988c] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2" @click.prevent="handleSubmit">
        Get Account
      </button>

      <p class="mt-4 text-center text-sm">
        Already have an account?
        <a href="http://localhost:8080/#/login" class="text-[#075e54] font-semibold mb-4">Login</a>
      </p>
    </div>
  </div>
</template>


  
<script>
  export default {
    name: 'SignUpForm',
    methods: {
      handleSubmit() {
        // Get the form data
        const formData = {
          username: document.getElementById('username').value,
          email: document.getElementById('email').value,
          password: document.getElementById('password').value,
          WABAID: document.getElementById('WABAID').value,
          PAccessToken: document.getElementById('PAccessToken').value,
          Phone_id: document.getElementById('Phone_id').value,
        };
  
        // Check for required fields
        if (!formData.username || !formData.email || !formData.password || !formData.WABAID || !formData.PAccessToken || !formData.Phone_id) {
          alert('Please fill in all required fields.');
          return;
        }
  
        // Send a request to your FastAPI endpoint
        fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // console.log(response)
          alert('Account created successfully!');
          // Clear the form fields
          document.querySelectorAll('input').forEach(input => input.value = '');
        } else if (data.detail) {
          alert(data.detail); // Show the error message from the API
        } else {
        
          alert('Failed to create account. Please try again.');
        }
      })
      .catch(error => console.error(error));
  }
  
  
    },
  };
  </script>
  
  
  
  <!-- <style scoped>
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    height: 100vh;
    overflow: hidden; /* Prevents body scroll */
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f4f4f4; /* Background color */
  }
  .signup-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 90vh;
    background-color: #f7f7f7;
    padding: 18px;
    box-sizing: border-box;
  }
  
  .signup-container {
    width: 100%;
    max-width: 500px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    background-color: #fff;
    box-sizing: border-box;
  }
  
  h2 {
    font-size: 24px;
    margin-bottom: 10px;
    text-align: center;
  }
  
  p {
    font-size: 14px;
    color: #666;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .auth-buttons {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  .auth-button {
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    padding: 10px;
    border-radius: 4px;
    font-size: 14px;
    color: #fff;
    width: 48%;
  }
  
  .auth-button img {
    width: 20px; /* Adjust size as needed */
    margin-right: 10px; /* Space between logo and text */
  }
  
  .auth-button.google {
    background-color: #0b0c0c;
    margin-right: 2%; /* Add margin-right to create space */
  }
  
  .auth-button.facebook {
    background-color: #0c0e0e;
  }
  
  .name-fields {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
  }
  
  .name-fields .input-group {
    flex: 1;
    margin-right: 10px;
  }
  
  .name-fields .input-group:last-child {
    margin-right: 0;
  }
  
  .input-group {
    margin-bottom: 2px; /* Reduced margin between input groups */
    text-align: center;
  }
  
  .input-group.full-width input[type="text"],
  .input-group.full-width input[type="email"],
  .input-group.full-width input[type="password"],
  .input-group.full-width input[type="tel"] {
    width: 100%;
    max-width: 100%;
    padding: 12px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  label {
    display: block;
    margin-bottom: -8px; /* Reduced margin below labels */
    font-size: 14px;
    font-weight:normal;
    text-align: left;
  }
  
  .phone-input {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  select {
    width: 25%;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px 0 0 4px;
    margin-right: -1px;
    box-sizing: border-box;
  }
  
  input[type="tel"] {
    width: 75%;
    border-radius: 0 4px 4px 0;
  }
  
  .submit-button {
    width: 100%;
    padding: 10px;
    background-color: #075e53;
    color: #fff;
    font-size: 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
    box-sizing: border-box;
  }
  
  .submit-button:hover {
    background-color: #23a455;
  }
  
  a {
    color: #075e53;
    text-decoration: none;
    cursor: pointer;
  }
  
  a:hover {
    text-decoration: underline;
  } 
  
  @media (max-width: 600px) {
    .signup-container {
      width: 100%;
      padding: 10px;
    }
  
    .auth-buttons {
      flex-direction: column;
    }
  
    .auth-button {
      width: 100%;
      margin-bottom: 10px;
    }
  
    .name-fields {
      flex-direction: column;
    }
  
    .name-fields .input-group {
      margin-right: 0;
      margin-bottom: 10px;
    }
  
    .input-group {
      margin-bottom: 10px;
    }
  
    input[type="text"],
    input[type="email"],
    input[type="password"],
    input[type="tel"] {
      width: 100%;
    }
  
    select {
      width: 30%;
    }
  
    .submit-button {
      width: 100%;
    }
  }
  </style> -->