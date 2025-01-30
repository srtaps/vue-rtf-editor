<template>
  <div class="vue-views" id="course-content">
    <Navbar />
    <div class="vue-views__container">
      <div v-if="loading" class="mt-16">Loading lesson...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <div v-if="!loading && !error" class=""></div>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const courseId = route.query.v;
const loading = ref(true);
const error = ref(null);

const fetchCourse = async () => {
  try {
    const response = await fetch(`http://localhost:5000/courses/${courseId}`);

    if (!response.ok) {
      throw new Error("Failed to fetch course");
    }

    const data = await response.json();

    console.log(data);
    // title.value = data.title;
    // info.value = data.info;
    // professor.value = data.professor;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchCourse();
});
</script>

<style scoped></style>
