<template>
  <div class="content-section p-4">
    <!-- Section Header -->
    <div class="flex flex-col md:flex-row justify-between mb-4">
      <div>
        <h2 class="text-xl md:text-2xl font-bold">Scheduled Broadcasts</h2>
        <p class="text-sm md:text-base">Your content for scheduled broadcasts goes here.</p>
      </div>
    </div>

    <!-- Broadcast List Table -->
    <div class="bg-[#f5f6fa] rounded-md p-4 mb-4 shadow-lg">
      <div class="overflow-x-auto max-h-[60vh] custom-scrollbar">
        <table class="w-full border-collapse">
          <thead>
            <tr class="bg-[#dddddd] text-center">
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">ID</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Broadcast Name</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Template</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Contacts</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Success</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Failed</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0">Status</th>
              <th class="p-2 text-left md:p-4 border-b-2 bg-[#dddddd] sticky top-0 z-10">Action</th>
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
              <td class="border-[#ddd] p-2 md:p-4 text-center">
                <button @click="DeleteScheduledBroadcast(broadcast.id)"
                  class="hover:bg-white rounded-full p-2 transition">
                  <lord-icon src="https://cdn.lordicon.com/skkahier.json" trigger="hover"
                  colors="primary:#ff5757,secondary:#000000"  style="width:32px;height:32px">
                  </lord-icon>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>




<script>

export default {
  name: 'BroadCast3',
  data() {
    return {
      broadcasts: [],

    }

  },
  async mounted() {

    await this.fetchScheduledBroadcastList();
    
    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);
  },
  methods: {

    async fetchScheduledBroadcastList() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://localhost:8000/scheduled-broadcast/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const ScheduledbroadcastList = await response.json();
        this.broadcasts = ScheduledbroadcastList.map(broadcast => ({
          id: broadcast.id,
          name: broadcast.name.split(' - ')[0],  // Extract the part before " - "
          template: broadcast.template,
          contacts: broadcast.contacts.join(' , '), // Join the array without quotes
          success: broadcast.success,
          failed: broadcast.failed,
          status: broadcast.status
        }));
      } catch (error) {
        console.error('Error fetching scheduled-broadcastlist:', error);
      }
    },

    async DeleteScheduledBroadcast(broadcast_id) {
      const token = localStorage.getItem('token');
      try {

        const response = await fetch(`http://localhost:8000/broadcasts-delete/${broadcast_id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        this.fetchScheduledBroadcastList();


      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    },

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
</style>

   -->