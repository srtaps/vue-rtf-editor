<template>
  <div id="home">
    <Navbar />
    <div class="btn-container">
      <a href="/new-lesson"
        ><button class="button button--add-post">+ Add New Lesson</button></a
      >
    </div>
    <div class="wrapper">
      <h1>Home</h1>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
</script>
