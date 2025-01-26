<template>
  <div class="vue-views" id="new-lesson">
    <Navbar />
    <div class="vue-views__container">
      <Editor />
    </div>
  </div>
</template>

<script setup>
import Editor from "@/components/Editor.vue";
import Navbar from "@/components/Navbar.vue";
</script>
