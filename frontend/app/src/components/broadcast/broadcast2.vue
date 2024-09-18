<template>
  <div class="content-section">
    <div class="flex flex-col md:flex-row justify-between mb-4">
      <div>
        <h2 class="text-xl md:text-2xl font-bold">Broadcast Messages</h2>
        <p class="text-sm md:text-base">Your content for broadcast messages goes here.</p>
      </div>

      <div>
        <button @click="showPopup = true"
          class="bg-[#075e54] text-[#f5f6fa] px-4 py-2 md:px-4 md:py-4 text-sm md:text-base rounded-md shadow-lg">
          New Broadcast
        </button>
      </div>
    </div>

    <PopUp v-if="showPopup" @close="showPopup = false">
       <form @submit.prevent="handleBroadcast" id="messageForm">
        <h3>New Broadcast</h3>
        <!-- <label>Broadcast Name</label>
        <input type="text" v-model="broadcastName" placeholder="Broadcast Name" required>

        <label>Recipients</label>
        <input type="text" v-model="recipients" placeholder="Enter phone numbers, comma-separated" required>

        <label for="templates">Choose a template</label>
        <select v-model="selectedTemplate" required>
          <option value="" disabled>Select your option</option>
          <option v-for="template in templates" :key="template.id" :value="template.id">{{ template.name }}</option>
        </select>
        <h3>Contacts</h3>
        <div class="CSVimportContainer">

          <label for="csvFile">Upload CSV:</label>
          <input type="file" @change="handleFileUpload" />
          <button @click.prevent="importCSV">Import</button>
          <a href="https://drive.google.com/file/d/1hVQErwmNN6eGN1zLBoniW_34-GzAtMwm/view?usp=sharing" target="_blank">
            Download Sample CSV</a>
        </div>

        
        <h3>Schedule</h3>
        <label>
          <input type="checkbox" v-model="isScheduled"> Schedule for later
        </label>

        <div v-if="isScheduled">
          <label>Schedule Date</label>
          <input type="date" v-model="scheduleDate" required>

          <label>Schedule Time</label>
          <input type="time" v-model="scheduleTime" required>
        </div>  -->


        <div class="mb-2">
          <label for="broadcastName" class="block text-sm font-medium">Broadcast Name</label>
          <input type="text" v-model="broadcastName" id="broadcastName" placeholder="Broadcast Name" required
            class="border border-gray-300 rounded px-3 py-2 w-full">
        </div>

        <div class="mb-2">
          <label for="recipients" class="block text-sm font-medium">Recipients</label>
          <input type="text" v-model="recipients" id="recipients" placeholder="Enter phone numbers, comma-separated"
            required class="border border-gray-300 rounded px-3 py-2 w-full">
        </div>

        <div class="mb-2">
          <label for="templates" class="block text-sm font-medium">Choose a template</label>
          <select v-model="selectedTemplate" id="templates" required
            class="border border-gray-300 rounded px-3 py-2 w-full">
            <option value="" disabled>Select your option</option>
            <option v-for="template in templates" :key="template.id" :value="template.id">{{ template.name }}</option>
          </select>
        </div>

        <div class="mb-1">
          <label for="csvFile" class="block text-sm font-semibold">Upload CSV for Contacts:</label>
          <input type="file" @change="handleFileUpload" class="mb-2 w-[60%] mr-1" />
          <button @click.prevent="importCSV" class="bg-[#23a455] text-[#f5f6fa] px-4 py-2 rounded">Import</button>
          <a href="https://drive.google.com/file/d/1hVQErwmNN6eGN1zLBoniW_34-GzAtMwm/view?usp=sharing" target="_blank"
            class="text-blue-500">Download Sample CSV</a>
        </div>

        <h3 class="text-lg font-semibold mb-1">Schedule <input type="checkbox" v-model="isScheduled"> </h3>
        <div v-if="isScheduled" class="flex justify-between">
          <div class="w-[50%]">
            <label for="scheduleDate" class="block text-sm font-medium">Schedule Date</label>
            <input type="date" v-model="scheduleDate" id="scheduleDate" required
              class="border border-gray-300 rounded px-3 py-2 w-full">
          </div>
          <div class="w-[50%]">
            <label for="scheduleTime" class="block text-sm font-medium">Schedule Time</label>
            <input type="time" v-model="scheduleTime" id="scheduleTime" required
              class="border border-gray-300 rounded px-3 py-2 w-full">
          </div>
        </div>

        <div class="mb-2 bg-gray-100 rounded-lg p-4 max-w-full shadow-md">
          <div class="overflow-x-auto max-h-[20vh] custom-scrollbar">
            <table class="contact-table w-full rounded-lg border-collapse">
              <thead>
                <tr class="bg-[#dddddd] text-center">
                  <th class="p-2 bg-[#dddddd] rounded sticky top-0">Select</th>
                  <th class="p-2 bg-[#dddddd] rounded sticky top-0">Name</th>
                  <th class="p-2 bg-[#dddddd] rounded sticky top-0">Phone Number</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="contact in contacts" :key="contact.id">
                  <td class="text-center p-2 md:p-4"><input type="checkbox" v-model="selectedContacts"
                      :value="contact.phone"></td>
                  <td class="text-left p-2 md:p-4">{{ contact.name }}</td>
                  <td class="text-left p-2 md:p-4">{{ contact.phone }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <button type="submit" class="bg-[#23a455] text-[#f5f6fa] px-4 py-2 rounded">{{ isScheduled ? 'Schedule Message'
          : 'Send Message' }}</button>
      </form>
      <div id="response"></div>
    </PopUp>

    <h3 class="text-xl md:text-2xs mb-4">Broadcast List</h3>
    <div class="broadcastListContainer bg-gray-100 rounded-lg p-4 max-w-full mx-auto shadow-md custom-scrollbar">
      <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
        <table class="w-full rounded-lg border-collapse">
          <thead>
            <tr class="bg-[#dddddd] text-center">
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">ID</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Broadcast Name</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Template</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Contacts</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Success</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Failed</th>
              <th class="p-2 md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="broadcast in broadcasts" :key="broadcast.id">
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ broadcast.id }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ broadcast.name }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ broadcast.template }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ broadcast.contacts }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ broadcast.success }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ broadcast.failed }}</td>
              <td class="border-[#ddd] p-2 md:p-4 text-left">{{ broadcast.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>

import PopUp from "../popups/popup"
export default {
  name: 'BroadCast2',

  components: {
    PopUp
  }
  ,
  data() {
    return {
      broadcastName: '',
      recipients: '',
      selectedTemplate: '',
      templates: [],
      contacts: [],
      broadcasts: [],
      file: null,
      selectedContacts: [],
      showPopup: false,
      scheduleDate: '',  // New data property for schedule date
      scheduleTime: '',
      isScheduled: false,


    };
  },
  async mounted() {
    await this.fetchTemplates();
    await this.fetchContacts();
    await this.fetchBroadcastList();

    // Fetch contacts when the component is mounted
  },
  methods: {


    async fetchTemplates() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/templates/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templateNames = await response.json();
        this.templates = templateNames.map(name => ({ id: name, name }));
      } catch (error) {
        console.error('Error fetching templates:', error);
      }
    },

    async fetchContacts() {

      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/contacts/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const contactList = await response.json();
        this.contacts = contactList.map(contact => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone
        }));
      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    },


    async fetchBroadcastList() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://localhost:8000/broadcast/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const broadcastList = await response.json();
        this.broadcasts = broadcastList.map(broadcast => ({
          id: broadcast.id,
          name: broadcast.name.split(' - ')[0],
          template: broadcast.template,
          contacts: broadcast.contacts.join(' , '),
          success: broadcast.success,
          failed: broadcast.failed,
          status: broadcast.status


        }));
      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    },

    formatDateTime(date) {
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');

      return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
    },

    updateRecipients() {
      this.recipients = this.selectedContacts.join(', ');
    },

    async sendMessage() {
      const phoneNumbers = this.recipients.split(',').map(num => num.trim());
      const selectedTemplate = this.selectedTemplate;
      const formattedDate = this.formatDateTime(new Date());
      const broadcastNameWithDate = `${this.broadcastName} - ${formattedDate}`;
      const responseDiv = document.getElementById('response');
      responseDiv.textContent = 'Sending...';
      const token = localStorage.getItem('token');

      try {
        const response = await fetch('http://localhost:8000/send-template-message/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            recipients: phoneNumbers,
            template: selectedTemplate,
            
          }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');

        }

        const result = await response.json();
        responseDiv.textContent = `Success: ${result.successful_messages}, Errors: ${result.errors.length}`;

        const logResponse = await fetch('http://localhost:8000/broadcast', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: broadcastNameWithDate,
            template: selectedTemplate,
            contacts: phoneNumbers,
            success: result.successful_messages,
            failed: result.errors.length,
            status: result.errors.length > 0 ? 'Partially Successful' : 'Successful'
          }),
        });

        if (!logResponse.ok) {
          throw new Error('Network response was not ok')


        }

        const logResult = await logResponse.json()

        console.log('Broadcast logged:', logResult);
        this.fetchBroadcastList();

      } catch (error) {
        console.error('Error sending messages:', error);
        responseDiv.textContent = 'Error sending messages.';
      }
    },
    handleBroadcast() {
      if (this.isScheduled) {
        this.scheduleBroadcast();
      } else {
        this.sendMessage();
      }
    },

    async scheduleBroadcast() {
      // Logic for scheduling a broadcast
      const phoneNumbers = this.recipients.split(',').map(num => num.trim());
      const selectedTemplate = this.selectedTemplate;
      const formattedDate = this.formatDateTime(new Date());
      const broadcastNameWithDate = `${this.broadcastName} - ${formattedDate}`;
      const responseDiv = document.getElementById('response');
      responseDiv.textContent = 'Scheduling...';
      const token = localStorage.getItem('token');

      // Combine date and time for scheduling
      const scheduledDatetime = new Date(`${this.scheduleDate}T${this.scheduleTime}`).toISOString();

      try {

        const logResponse = await fetch('http://localhost:8000/broadcast', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: broadcastNameWithDate,
            template: selectedTemplate,
            contacts: phoneNumbers,
            success: 0,
            failed: 0,
            status: 'Scheduled',
            scheduled_time: scheduledDatetime,
            // task_id:result.task_id
          }),
        });

        if (!logResponse.ok) {
          throw new Error('Network response was not ok');
        }

        const logResult = await logResponse.json();
        console.log('Broadcast logged:', logResult);

        const response = await fetch(`http://localhost:8000/schedule-template-message/?scheduled_time=${encodeURIComponent(scheduledDatetime)}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            recipients: phoneNumbers,
            template: selectedTemplate,
            broadcast_id: logResult.broadcast_id
            // scheduled_time: scheduledDatetime // Send the scheduled datetime to backend
          }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();

        // Update the log entry with the task_id
        const updateLogResponse = await fetch(`http://localhost:8000/broadcast/${logResult.broadcast_id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            task_id: result.task_id,  // Include task_id from scheduling response
          }),
        });

        if (!updateLogResponse.ok) {
          throw new Error('Network response was not ok');
        }

        const updateLogResult = await updateLogResponse.json();
        console.log('Broadcast log updated with task_id:', updateLogResult);

        responseDiv.textContent = 'Broadcast scheduled successfully.';

        this.fetchBroadcastList();
      } catch (error) {
        console.error('Error scheduling broadcast:', error);
        responseDiv.textContent = 'Error scheduling broadcast.';
      }
    },

    handleFileUpload(event) {
      this.file = event.target.files[0];
    },

    async importCSV() {
      if (!this.file) {
        alert('Please select a file to import.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const response = await fetch('http://localhost:8000/import-contacts', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.contacts = data.contacts;
        alert('Contacts imported successfully!');

        // Append phone numbers to the recipients input field
        const phoneNumbers = this.contacts.map(contact => contact.phone).join(',');
        this.recipients = this.recipients ? this.recipients + ',' + phoneNumbers : phoneNumbers;
      } catch (error) {
        console.error(error);
        alert('Failed to import contacts.');
      }
    },

  },
  watch: {
    selectedContacts: function () {
      this.updateRecipients();
    }
  }
};
</script>

<style scoped>
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



















<!-- <style>
.NeWBroadcastButtonContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  max-width: 1100px;
  padding: 20px;
  display: flex;
  margin-bottom: 20px;

  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.NeWBroadcastButtonContainer button {
  margin-left: 725px;

}

.broadcastListContainer {
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

.broadcastList-table {
  width: 100%;
  border-radius: 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;
  /* Adjust height as needed */

}

th {
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;


}

.broadcastList-table td {
  border: 1px solid #ddd;

  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.broadcastList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;

}

.broadcastList-table tbody {
  background-color: white;
}

.CSVimportContainer {
  display: flex;
  align-items: center;

}

.CSVimportContainer a {
  padding-left: 10px;
}

.CSVimportContainer input {
  max-width: 200px;
  margin-top: 20px;
  margin-left: 10px;
}

.CSVimportContainer button {
  margin-left: 10px;
  height: 35px;
}


#response {
  margin-top: 20px;
  font-size: 16px;
  color: #333;
}

.contact-table {
  width: auto;

  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 200px;
  /* Adjust height as needed */

  margin-bottom: 20px;
}


.contact-table td {
  padding: 15px;
  text-align: left;
  border-collapse: collapse;
  background-color: #ffffff;
}

.contact-table th {
  padding: 15px;
  text-align: left;
  border-collapse: collapse;
}


.contact-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
}
</style> -->
