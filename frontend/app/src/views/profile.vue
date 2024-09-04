<!-- FOR A POPUP VIEW -->

<!-- <template>
  <div class="overlay" v-if="visible" @click.self="close">
    <div class="popup">
      <h2>Profile Details</h2>
      <form @submit.prevent="saveProfile">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="localUser.email" />

        <label for="name">Name:</label>
        <input type="text" id="name" v-model="localUser.name" />

        <label for="whatsapp_business_id">WhatsApp Business ID:</label>
        <input type="text" id="whatsapp_business_id" v-model="localUser.whatsapp_business_id" />

        <label for="phone_id">Phone ID:</label>
        <input type="text" id="phone_id" v-model="localUser.phone_id" />

        <label for="access_token">Access Token:</label>
        <input type="text" id="access_token" v-model="localUser.access_token" />

        <button type="submit">Save</button>
        <button type="button" @click="close">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfilePopup',
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localUser: { ...this.user } 
    };
  },
  watch: {
    visible: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchUserDetails();
        }
      }
    },
    user: {
      immediate: true,
      handler(newVal) {
        this.localUser = { ...newVal }; // Sync localUser with the user prop
      }
    }
  },
  methods: {
    close() {
      this.$emit('close');
    },
    async fetchUserDetails() {
      try {
        const response = await fetch('http://localhost:8000/user', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user details');
        }

        const data = await response.json();
        this.localUser.email = data.email;
        this.localUser.name = data.name;
        this.localUser.whatsapp_business_id = data['Whatsapp_Business_Id'];
        this.localUser.phone_id = data['Phone_id'];
        this.localUser.access_token = data['Access_Token'];
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },
    async saveProfile() {
      try {
        const response = await fetch('http://localhost:8000/user', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({
            email: this.localUser.email,
            name: this.localUser.name,
            Whatsapp_Business_Id: this.localUser.whatsapp_business_id,
            Phone_id: this.localUser.phone_id,
            Access_Token: this.localUser.access_token
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to save user details');
        }

        console.log('Profile saved', this.localUser);
        this.$emit('update:user', this.localUser); 
        this.close();
      } catch (error) {
        console.error('Error saving user details:', error);
      }
    }
  }
};
</script>
  
<style scoped>
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .popup {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 300px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  form {
    display: flex;
    flex-direction: column;
  }
  
  label {
    margin-top: 10px;
  }
  
  input {
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    padding: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  button[type="submit"] {
    background-color: #075e54;
    color: white;
  }
  
  button[type="button"] {
    background-color: #ddd;
  }
</style> -->





<!-- FOR A SIDEBAR VIEW -->

<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

  <div class="profile-sidebar-overlay" v-if="visible" @click.self="close">
    <div class="profile-sidebar">
      <div class="header">
        <h2>Profile Details</h2>
        <span class="cancel-icon" @click="close">
          <i class="fas fa-times"></i>
        </span>
      </div>
      <form @submit.prevent="saveProfile">
        <div>
          <label for="email">Email:</label>
          <div class="input-group">
            <input type="email" id="email" v-model="localUser.email" :readonly="isEmailReadonly" />
            <span class="edit-icon" @click="toggleEmailReadonly">
              🖉
            </span>
          </div>
        </div>
        <div>
          <label for="name">Name:</label>
          <div class="input-group">
            <input type="text" id="name" v-model="localUser.name" :readonly="isNameReadonly" />
            <span class="edit-icon" @click="toggleNameReadonly">
              🖉
            </span>
          </div>
        </div>

        <label for="whatsapp_business_id">WhatsApp Business ID:</label>
        <input type="text" id="whatsapp_business_id" v-model="localUser.whatsapp_business_id" readonly />

        <label for="phone_id">Phone ID:</label>
        <input type="text" id="phone_id" v-model="localUser.phone_id" readonly />

        <label for="access_token">Access Token:</label>
        <input type="text" id="access_token" v-model="localUser.access_token" readonly />

        <button type="submit">Save</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileSidebar',
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localUser: { ...this.user },
      isEmailReadonly: true,
      isNameReadonly: true
    };
  },
  watch: {
    visible: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchUserDetails();
        }
      }
    },
    user: {
      immediate: true,
      handler(newVal) {
        this.localUser = { ...newVal };
      }
    }
  },
  methods: {
    close() {
      this.$emit('close');
    },
    toggleEmailReadonly() {
      this.isEmailReadonly = !this.isEmailReadonly;
    },
    toggleNameReadonly() {
      this.isNameReadonly = !this.isNameReadonly;
    },
    async fetchUserDetails() {
      try {
        const response = await fetch('http://localhost:8000/user', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user details');
        }

        const data = await response.json();
        this.localUser.email = data.email;
        this.localUser.name = data.name;
        this.localUser.whatsapp_business_id = data['Whatsapp_Business_Id'];
        this.localUser.phone_id = data['Phone_id'];
        this.localUser.access_token = data['Access_Token'];
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },
    async saveProfile() {
      try {
        const response = await fetch('http://localhost:8000/user', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
          body: JSON.stringify({
            email: this.localUser.email,
            name: this.localUser.name,
            Whatsapp_Business_Id: this.localUser.whatsapp_business_id,
            Phone_id: this.localUser.phone_id,
            Access_Token: this.localUser.access_token
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to save user details');
        }

        console.log('Profile saved', this.localUser);
        this.$emit('update:user', this.localUser);
        this.close();
      } catch (error) {
        console.error('Error saving user details:', error);
      }
    }
  }
};
</script>

<style scoped>

.profile-sidebar-overlay {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  z-index: 1000;
}

.profile-sidebar {
  width: 300px;
  right: 0;
  height: 100%;
  background: white;
  padding: 20px;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  transform: translateX(100%);
  transition: transform 0.3s ease-in-out;
}

.profile-sidebar-overlay .profile-sidebar {
  transform: translateX(0);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 2vw 0 4vw 0;
}

h2 {
  margin: 0;
}

.cancel-icon {
  cursor: pointer;
  color: #075e54; 
  font-size: 18px; 
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-top: 10px;
}

input {
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.input-group {
    display: flex;
    align-items: center;
    position: relative;
}

.edit-icon {
    position: absolute;
    right: 10px; 
    cursor: pointer;
    color: #007bff; 
}

input#email,
input#name {
  padding-right: 30px; 
}

button {
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

button[type="submit"] {
  background-color: #075e54;
  color: white;
}

button[type="button"] {
  background-color: #ddd;
  color: #075e54;
}
</style>