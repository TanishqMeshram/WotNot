<template>
  <div class="content-section p-4">
    <div class="flex flex-col md:flex-row justify-between mb-4">
      <div>
        <h2 class="text-xl md:text-2xl font-bold">Manage Templates</h2>
        <p class="text-sm md:text-base">Your content for scheduled broadcasts goes here.</p>
      </div>

      <div class="bg-[#075e54] rounded-md shadow-lg mt-2 md:mt-0">
        <button @click="showSelectionPopup = true" class="text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base w-full md:w-auto">Create New Template</button>
      </div>
    </div>

    <div class="bg-[#f5f6fa] rounded-md p-4 mb-4 shadow-lg">
      <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
        <table class="w-full rounded-md border-collapse">
          <thead>
            <tr class="bg-[#dddddd] text-center">
              <th class="p-2 text-center md:p-4 border-[#ddd] sticky top-0 bg-[#dddddd]">Name</th>
              <th class="p-2 text-center md:p-4 border-[#ddd] sticky top-0 bg-[#dddddd]">Language</th>
              <th class="p-2 text-center md:p-4 border-[#ddd] sticky top-0 bg-[#dddddd]">Status</th>
              <th class="p-2 text-center md:p-4 border-[#ddd] sticky top-0 bg-[#dddddd]">Category</th>
              <th class="p-2 text-center md:p-4 border-[#ddd] sticky top-0 bg-[#dddddd]">Sub Category</th>
              <th class="p-2 text-center md:p-4 border-[#ddd] sticky top-0 bg-[#dddddd]">ID</th>
              <th class="p-2 text-center md:p-4 border-[#ddd] sticky top-0 bg-[#dddddd]">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="template in templates" :key="template.id">
              <td class=" border-[#ddd] p-2 md:p-4 text-left">{{ template.name }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.language }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.status }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.category }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.sub_category }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">{{ template.id }}</td>
              <td class=" border-[#ddd] p-2 md:p-4 text-center">
                <button @click="deleteTemplate(template.id)" class="text-red-500 hover:text-red-700">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 p-0 text-red-500"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M3 6h18M4 6h16l-1 14H5L4 6z"></path>
                    <path d="M10 11v6m4-6v6"></path>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showSelectionPopup" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50" @click.self="closeSelectionPopup">
      <div class="bg-white p-4 rounded-md shadow-lg max-w-[90vw] md:max-w-md w-full">
        <h2 class="text-lg font-bold mb-4">Select Template Type</h2>
        <div class="flex flex-col md:flex-row justify-between gap-4">
          <button @click="selectType('MARKETING')" class="flex-1 p-2 bg-[#075e54] text-white rounded-md cursor-pointer hover:bg-[#063a41]">Marketing</button>
          <button @click="selectType('UTILITY')" class="flex-1 p-2 bg-[#075e54] text-white rounded-md cursor-pointer hover:bg-[#063a41]">Utility</button>
        </div>
        <button @click="closeSelectionPopup" class="mt-4 bg-[#ff4d4d] text-white border-none p-2 rounded-md cursor-pointer">Close</button>
      </div>
    </div>

    <div v-if="showPopup" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50" @click.self="closePopup">
      <div class="bg-white p-4 rounded-md shadow-lg max-w-[90vw] md:max-w-md w-full">
        <h2 class="text-lg font-bold mb-4">Create {{ selectedType }} Template</h2>
        <form @submit.prevent="submitTemplate">
          <input 
            v-model="template.name" 
            placeholder="Template Name" 
            @blur="validateTemplateName" 
            :class="{ 'border-red-500': nameError }" 
            required 
            class="border border-[#ddd] p-2 rounded-md w-full mb-2"
          />
          <span v-if="nameError" class="text-red-500 text-sm mb-2">{{ nameError }}</span>
          <textarea v-model="bodyComponent.text" placeholder="Body Text" required class="border border-[#ddd] p-2 rounded-md w-full mb-2"></textarea>

          <input v-model="headerComponent.text" placeholder="Header Text (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />

          <input v-model="footerComponent.text" placeholder="Footer Text (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />

          <input v-if="selectedSubCategory !== 'ORDER_STATUS'" v-model="button.text" placeholder="Button Text (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />
          <input v-if="selectedSubCategory !== 'ORDER_STATUS'" v-model="button.url" placeholder="Button URL (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />

          <select v-model="selectedSubCategory" required class="border border-[#ddd] p-2 rounded-md w-full mb-4">
            <option value="" disabled>Select Sub-Category</option>
            <option value="ORDER_DETAILS">Order Details</option>
          </select>

          <button type="submit" class="bg-[#5cb85c] text-white border-none p-2 rounded-md cursor-pointer mb-4 hover:bg-[#4cae4c]">Submit</button>
        </form>
        <button @click="closePopup" class="bg-[#ff4d4d] text-white border-none p-2 rounded-md cursor-pointer">Close</button>
      </div>
    </div>
  </div>
</template>





<script>
import axios from 'axios';

export default {
  name: 'BroadCast1',
  data() {
    return {
      templates: [],
      showPopup: false,
      showSelectionPopup: false,
      selectedType: '',
      selectedSubCategory: '',
      template: {
        name: '',
        components: []
      },
      bodyComponent: {
        type: 'BODY',
        text: ''
      },
      headerComponent: {
        type: 'HEADER',
        format: 'TEXT',
        text: ''
      },
      footerComponent: {
        type: 'FOOTER',
        text: ''
      },
      button: {
        type: 'URL',
        text: '',
        url: ''
      },
      nameError: ''
    };
  },

  async mounted() {
    await this.fetchtemplateList();
  },

  methods: {
    async fetchtemplateList() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch("http://localhost:8000/template", {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templatelist = await response.json();
        this.templates = templatelist.data;
      } catch (error) {
        console.error("There was an error fetching the templates:", error);
      }
    },

    selectType(type) {
      this.selectedType = type;
      this.showSelectionPopup = false;
      this.showPopup = true;
    },

    validateTemplateName() {
      const regex = /^[a-z]+$/;
      if (!regex.test(this.template.name)) {
        this.nameError = 'Template name must contain only lowercase letters.';
      } else {
        this.nameError = '';
      }
    },

    async submitTemplate() {
      if (this.nameError) {
        return; // Prevent form submission if there are validation errors
      }
      
      this.template.components = [this.bodyComponent];

      if (this.selectedSubCategory !== 'ORDER_STATUS') {
        if (this.headerComponent.text) {
          this.template.components.push(this.headerComponent);
        }

        if (this.footerComponent.text) {
          this.template.components.push(this.footerComponent);
        }

        if (this.button.text && this.button.url) {
          this.template.components.push({
            type: 'BUTTONS',
            buttons: [this.button]
          });
        }
      } else {
        if (this.footerComponent.text) {
          this.template.components.push(this.footerComponent);
        }
      } 
      
      const payload = {
        name: this.template.name,
        components: this.template.components,
        language: 'en_US',
        category: this.selectedType,
        sub_category: this.selectedSubCategory
      };

      const token = localStorage.getItem('token');

      if (!token) {
        console.error('No access token found in local storage');
        return;
      }

      try {
        const response = await axios.post('http://localhost:8000/create-template', payload, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        console.log('Template created successfully:', response.data);

        await this.fetchtemplateList();
        this.closePopup();
      } catch (error) {
        console.error('Error creating template:', error.response ? error.response.data : error.message);
      }
    },

    closeSelectionPopup() {
      this.showSelectionPopup = false;
      this.selectedType = '';
    },
    closePopup() {
      this.showPopup = false;
      this.template.name = '';
      this.bodyComponent.text = '';
      this.headerComponent.text = '';
      this.footerComponent.text = '';
      this.button.text = '';
      this.button.url = '';
      this.selectedSubCategory = '';
    }
  }
}
</script>



<style scoped>

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px; 
}

.custom-scrollbar::-webkit-scrollbar-track {
  border-radius: 16px;
  background-color: #e7e7e7;
  border: 1px solid #cacaca;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  border-radius: 8px;
  border: 3px solid transparent;
  background-clip: content-box;
  background-color: #075e54;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #555; 
}


</style>






<!-- <style scoped>

.error {
  border-color: red;
}

.error-message {
  color: red;
  font-size: 0.875em;
  margin-top: 0.5em;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}

.CreateTemplateContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  max-width: 1100px;
  padding: 20px;
  display: flex;
  margin-bottom: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.CreateTemplateContainer button {
  margin-left: 805px;
}

.templateList_container {
  background-color: #f5f6fa;
  border-radius: 12px 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.templateList-table {
  width: 100%;
  border-radius: 12px 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;
}

th {
  padding: 20px 43px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.templateList-table td {
  border: 1px solid #ddd;
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.templateList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.templateList-table tbody {
  background-color: white;
}

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}

.template-type-options {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.template-type-options button {
  flex: 1;
  padding: 10px;
  border: none;
  background-color: #075e54;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.template-type-options button:hover {
  background-color: #075e54;
}

.discard-button {
  margin-top: 20px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button {
  background-color: 5;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #218838;
}
</style>  -->
