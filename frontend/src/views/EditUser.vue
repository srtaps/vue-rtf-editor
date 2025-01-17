<template>
  <div class="vue-views" id="users">
    <Navbar />
    <div class="vue-views__container">
      <h2>Edit user</h2>
      <p>User ID: {{ userId }}</p>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { useRoute } from "vue-router";

const route = useRoute();
const userId = route.query.userId;
</script>

<style scoped></style>
