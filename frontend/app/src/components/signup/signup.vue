<template>
    <div style="height: 100vh; overflow-y: auto;" ref="scrollContainer" class="signup-wrapper">
      <div class="signup-wrapper">
      <div class="signup-container">
        <h2>Get started with an account on Wotnot</h2>
        <br>
  
        <div class="name-fields">
    <div class="input-group full-width">
      <label for="username">Business Name</label>
      <input type="username" id="username" placeholder="Business Name" required />
    </div>
  </div>
  <div class="input-group full-width">
    <label for="email">Business Email Address</label>
    <input type="email" id="email" placeholder="Business Email Address" required />
  </div>
  <div class="input-group full-width">
    <label for="password">Password</label>
    <input type="password" id="password" placeholder="Password" required />
  </div>
  <div class="input-group full-width">
    <label for="WABAID">Whatsapp Business account ID</label>
    <input type="WABAID" id="WABAID" placeholder="Whatsapp Business account ID" required />
  </div>
  <div class="input-group full-width">
    <label for="PAccessToken">Permanent Access Token</label>
    <input type="PAccessToken" id="PAccessToken" placeholder="Permanent Access Token" required />
  </div>
  <div class="input-group full-width">
    <label for="Phone_id">Phone number ID</label>
    <input type="Phone_id" id="Phone_id" placeholder="Phone number ID" required />
  </div>
  
  
        <!--<div class="input-group full-width">
          <label for="phone">Your mobile number</label>
          <div class="phone-input">
            <select id="phone-code">
              <option value="IN" data-code="+91">🇮🇳 +91</option>
              <option value="US" data-code="+1">🇺🇸 +1</option>
              <option value="GB" data-code="+44">🇬🇧 +44</option>
              <option value="CA" data-code="+1">🇨🇦 +1</option>
              <option value="AU" data-code="+61">🇦🇺 +61</option>
              <option value="DE" data-code="+49">🇩🇪 +49</option>
              <option value="FR" data-code="+33">🇫🇷 +33</option>
              <option value="JP" data-code="+81">🇯🇵 +81</option>
              <option value="CN" data-code="+86">🇨🇳 +86</option>
              <option value="BR" data-code="+55">🇧🇷 +55</option>
             
            </select>
            <input type="tel" id="phone" placeholder="Your mobile number" required />
          </div>
        </div>-->
  
        <div class="input-group">
          <p>
            By signing up you agree to the
            <a href="#">Terms</a> and <a href="#">Privacy Policy</a>
          </p>
        </div>
  
        <button class="submit-button" @click.prevent="handleSubmit">Get Account</button>
  
        <p>Already have an account? <a href="http://localhost:8080/#/login">login</a></p>
      </div>
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
  
  
  
  <style scoped>
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
    background-color: #075e53;
    margin-right: 2%; /* Add margin-right to create space */
  }
  
  .auth-button.facebook {
    background-color: #075e53;
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
    font-weight: bold;
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
  </style>