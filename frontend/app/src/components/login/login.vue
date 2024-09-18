<template>
  <main class="flex items-center justify-center min-h-screen bg-gray-100 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-sm bg-white p-8 rounded-lg shadow-md">
      <h2 class="text-2xl sm:text-3xl font-semibold text-center text-gray-800 mb-4">
        Login to your <br> Wotnot account
      </h2>

      <hr class="my-6 border-gray-300" />

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Email</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required 
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" 
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" 
          />
        </div>
        <button 
          type="submit" 
          class="w-full bg-[#075e54] text-white py-2 rounded-md hover:bg-[#2d988c] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          Login
        </button>
        <p v-if="errorMessage" class="text-red-500 text-sm mt-2">{{ errorMessage }}</p>
      </form>

      <p class="mt-4 text-center text-sm">
        Don't have an account? 
        <a href="http://localhost:8080/#/login/signup" class="text-[#075e54] font-semibold mb-4">Sign Up</a>
      </p>
    </div>
  </main>
</template>


<script>
  export default {
    name:"LoginPage",
    data() {
      return {
        username: '',
        password: '',
        errorMessage: '',
      };
    },
    methods: {
      async handleLogin() {
        fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: this.username,
      password: this.password
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.access_token) {
      // Store the token in localStorage or Vuex (if using Vuex)
      localStorage.setItem('token', data.access_token);
      // Redirect to the dashboard
      console.log()
      this.$router.push('/dashboard');
    } else {
      // Handle login error
      alert('Login failed');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
      },
    },
  };
  </script>
