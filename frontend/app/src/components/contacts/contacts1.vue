<template>
  <div class="content-section">
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-xl md:text-2xl font-bold ">Manage Contacts</h2>
        <p class="text-xsm md:text-base">Contact list stores the list of numbers that you've interacted with.
          You can even manually export or import contacts.</p>
      </div>
      

      <div>
        <button @click="showPopup = true"
          class="bg-[#075e54] text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base rounded-md shadow-lg">
          + Add Contact
        </button>
      </div>
    </div>
    <PopUp1 v-if="showPopup" @close="closePopup">
      <form @submit.prevent="submitForm" id="contactForm" class="p-6 w-[400px]">
        <h2 class="text-xl font-semibold mb-4">{{ isEditing ? 'Edit Contact' : 'Add Contact' }}</h2>
        <hr class="mb-4" />

        <div class="mb-4">
          <label for="name" class="block text-sm font-medium">Name<span class="text-red-800">*</span></label>
          <input type="text" v-model="contact.name" id="name" placeholder="Name" required
            class="border border-gray-300 rounded px-3 py-2 w-full">
        </div>

        <div class="mb-4">
          <label for="phone" class="block text-sm font-medium">Phone Number<span class="text-red-800">*</span></label>
          <div class="flex">
            <select v-model="contact.countryCode" class="border border-gray-300 rounded-l px-3 py-2 w-20 mr-2">
              <option value="+1">+1</option>
              <option value="+44">+44</option>
              <option value="+91">+91</option>
            </select>
            <input type="text" v-model="contact.phone" id="phone" placeholder="Phone Number" required
              class="border border-gray-300 rounded-r px-3 py-2 w-full">
          </div>
        </div>
        <label for="email" class="block text-sm font-medium">Email<span class="text-red-800">*</span></label>
        <input type="email" v-model="contact.email" id="email" placeholder="Email" required
          class="border border-gray-300 rounded px-3 py-2 mb-2 w-full">
        
        
        <label for="email" class="block text-sm font-medium">Tags</label>
        <input type="text" v-model="contact.tags" id="tags" placeholder="Tags (comma separated)"
          class="border border-gray-300 rounded px-3 py-2 mb-2 w-full">

        <div class="flex justify-between mt-6">
          <button @click="closePopup" type="button"
            class="border-[2px] bg-gray-200 hover:bg-[#c2c1c1] text-black rounded-lg px-4 py-2 ">
            Cancel
          </button>
          <button type="submit" class="bg-[#23a455] text-white px-4 py-2 rounded">
            Save
          </button>
        </div>
      </form>
    </PopUp1>

    <h3 class="text-xl md:text-2xs mb-4 text-gray-600"><b>Contact List</b></h3>
    
    
      <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
        <table class="w-full rounded-lg border-collapse block">
          <thead>
            <tr class="bg-[#ffffff] border-b-2 border-gray-300" >
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Id</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Name</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Phone Number</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Email</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Tags</th>
              <th class="py-5 px-3 border-white m-2 text-left bg-[#ffffff] sticky top-0">Created at</th>
              <th class="py-5 px-3 border-white m-2 text-center bg-[#ffffff] sticky top-0 z-10">Action</th>
            </tr>
          </thead>

          <tbody class="bg-white">
            <tr v-for="contact in contacts" :key="contact.id">
              <td class="border-gray-300 py-5 px-3">{{ contact.id }}</td>
              <td class="border-gray-300 py-5 px-3">{{ contact.name }}</td>
              <td class="border-gray-300 py-5 px-3">{{ contact.phone }}</td>
              <td class="border-gray-300 py-5 px-3">{{ contact.email }}</td>
              <td class="border-gray-300 py-5 px-4 w-[10%]">{{ contact.tags.join(', ') }}</td>
              <td class="border-gray-300 py-5 px-3">{{ formatDate(contact.created_at) }}</td>
              <td class="border-gray-300 py-5 px-3">
                <div class="flex justify-center">
                  <button @click="modifyContact(contact)" class="hover:bg-white rounded-full p-2 transition">
                    <lord-icon src="https://cdn.lordicon.com/wuvorxbv.json" trigger="hover"
                      style="width:32px;height:32px">
                    </lord-icon>
                  </button>
                  <button @click="deleteContact(contact.phone)"
                    class="hover:bg-white rounded-full p-2 transition">
                    <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                      colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
                    </lord-icon>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification';
import PopUp1 from "../popups/popup1";
// import PopUpSmall from "../popups/popup_small";
export default {
  components: {
    PopUp1,
    // PopUpSmall
  },
  async mounted() {
    await this.fetchContactList();

    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);
  },
  name: "ContActs1",
  data() {
    return {
      showPopup: false,
      showActionPopup: false,
      contact: {
        id: "",
        name: "",
        email: "",
        phone: "",
        countryCode: "+91",
        tags: "",
      },
      selectedContact: null,
      contacts: [],
      isEditing: false
    };
  },
  methods: {

  async submitForm() {
  const toast= useToast()
  const { id, name, email, phone, countryCode, tags } = this.contact;

  let fullPhoneNumber = phone;
  if (countryCode && countryCode.trim() !== '') {
    fullPhoneNumber = `${countryCode} ${phone}`;
  }

  const tagArray = Array.isArray(tags)
    ? tags
    : typeof tags === 'string'
      ? tags.split(",").map(tag => tag.trim()).filter(tag => tag.length > 0) // Ensure no empty tags
      : [];

  const url = id ? `http://localhost:8000/contacts/${id}` : "http://localhost:8000/contacts/";
  const method = id ? "PUT" : "POST";
  const token = localStorage.getItem("token");

  try {
    const response = await fetch(url, {
      method: method,
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, phone: fullPhoneNumber, tags: tagArray }), // Send full phone number
    });

    if (response.ok) {
      if (id) {
      toast.success("Contact updated successfully");
    } else {
      toast.success("Contact created successfully");
    }
      this.clearForm();
      this.fetchContactList();
    } else {
      const errorData = await response.json();
      toast.error(`Error: ${errorData.detail}`);
    }
  } catch (error) {
    console.error("Error saving contact:", error);
    alert("Error saving contact");
  }
},


    clearForm() {
      this.contact = {
        id: "",
        name: "",
        email: "",
        phone: "",
        tags: "",
      };
      this.showPopup = false;
    },
    closePopup() {
      this.showPopup = false;
      this.clearForm();  // Clear the form when closing the popup
    },

    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', options).replace(/,/g, '');
    },

    async fetchContactList() {
      const token = localStorage.getItem("token");
      try {
        const response = await fetch("http://localhost:8000/contacts/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const contactsList = await response.json();
        console.log(contactsList)
        this.contacts = contactsList.map((contact) => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone,
          email: contact.email,
          tags: contact.tags,
          created_at: this.formatDate(contact.created_at),
        }));
      } catch (error) {
        console.error("Error fetching contact:", error);
      }
    },
    // openActionPopup(contact) {
    //   this.selectedContact = contact;
    //   this.showActionPopup = true;
    // },
    closeActionPopup() {
      this.showActionPopup = false;
      this.selectedContact = null;
    },
    modifyContact(contact) {
      this.selectedContact = contact;
      this.contact = { ...this.selectedContact };
      this.showPopup = true;
      this.closeActionPopup();
    },
    async deleteContact(phone) {
      const toast= useToast()
      const confirmDelete = confirm("Are you sure you want to delete this contact?");
      if (!confirmDelete) return;

      const token = localStorage.getItem("token");
      try {
        const response = await fetch(`http://localhost:8000/contacts/${phone}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          toast.success("Contact deleted successfully");
          this.fetchContactList();
          this.closeActionPopup();
        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error("Error deleting contact:", error);
        alert("Error deleting contact");
      }
    },
  },
};
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










<!-- <div class="mb-4">
          <label for="attributes" class="block text-sm font-medium">Custom Attribute (Optional)</label>
          <button @click="addAttribute" type="button" class="border border-green-500 text-green-500 px-4 py-2 rounded">
            + Add Attribute
          </button>
        </div> -->

<!-- <PopUpSmall v-if="showActionPopup" @close="closeActionPopup">
      <div class="bg-white shadow-lg rounded-lg p-4">
        <p class="text-lg mb-4">What action do you want to take?</p>
        <div class="flex space-x-4">
          <button @click="modifyContact" class="bg-yellow-500 text-white py-2 px-4 rounded">Modify</button>
          <button @click="deleteContact(selectedContact.phone)"
            class="bg-red-500 text-white py-2 px-4 rounded">Delete</button>
        </div>
      </div>
    </PopUpSmall> -->
<!-- <button @click="openActionPopup(contact)"
                  class="bg-[#075e54] text-white py-2 px-4 rounded">Action
                </button> -->
















<!-- <style scoped>
 .contactsListContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

}

.contactsList-table {
  width: 100%;
  border-radius: 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;

}

th {
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;


}

.contactsList-table td {
  border: 1px solid #ddd;

  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.contactsList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;

}

.contactsList-table tbody {
  background-color: white; 
}


</style>  -->
