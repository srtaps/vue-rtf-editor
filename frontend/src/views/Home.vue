<template>
  <div class="vue-views" id="home">
    <Navbar />
    <div class="vue-views__container">
      <h1>Home</h1>

      <div v-if="loading" class="mt-16">Loading users...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <div v-else class="cards-grid mt-16">
        <div
          v-for="course in courses"
          :key="course.course_id"
          class="course-card"
        >
          <div class="course-content">
            <h2>{{ course.title }}</h2>
            <p class="info">{{ course.info }}</p>
            <p class="professor">Professor: {{ course.professor }}</p>
          </div>
          <button class="button button--submit mt-16">Visit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { ref, onMounted } from "vue";

const courses = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchCourses = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await fetch("http://localhost:5000/courses");
    if (!response.ok) {
      throw new Error("Failed to fetch courses");
    }
    courses.value = await response.json();
  } catch (err) {
    error.value = "Error loading courses. Please try again later.";
    console.error("Error:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchCourses();
});
</script>

<style scoped>
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.course-card {
  background: #2c2c38;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.course-card:hover {
  transform: translateY(-4px);
}

.course-card h2 {
  margin-bottom: 12px;
  font-size: 1.2em;
}

.course-card .info {
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.course-card .professor {
  font-size: 0.96rem;
  font-style: italic;
}
</style>
