<template>
    <div class="fixed inset-0 bg-black bg-opacity-20 flex justify-center items-center p-5 z-[10000] text-left shadow-lg">
      <div class="bg-[#f5f6fa] p-5 rounded-md w-[700px] overflow-y-auto relative">
        <span class="close relative flex right-[-98%] text-xl hover:cursor-pointer" @click="$emit('close')">&times;</span>   
        <slot/>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PopUp'
  }
  </script>
  