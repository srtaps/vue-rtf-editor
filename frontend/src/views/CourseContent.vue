<template>
  <div class="vue-views" id="course-content">
    <Navbar />
    <div class="vue-views__container">
      <div v-if="loading" class="mt-16">Loading lesson...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <div v-if="!loading && !error" class="">
        <div class="lesson-nav">
          <p class="text-bold">{{ course.title }}</p>
          <ul class="mt-16">
            <li v-for="lesson in lessons" :key="lesson.lesson_id">
              <p @click="selectLesson(lesson)">{{ lesson.title }}</p>
            </li>
          </ul>
        </div>
        <div class="lesson-content" v-if="selectedLesson">
          <h2>{{ selectedLesson.title }}</h2>
          <div v-html="selectedLesson.content"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const courseId = route.query.v;
const course = ref(null);
const lessons = ref([]);
const selectedLesson = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchCourse = async () => {
  try {
    const [courseResponse, lessonsResponse] = await Promise.all([
      fetch(`http://localhost:5000/courses/${courseId}`),
      fetch(`http://localhost:5000/course/${courseId}/lessons`),
    ]);

    if (!courseResponse.ok) {
      throw new Error("Failed to fetch course data");
    }
    if (!lessonsResponse.ok) {
      throw new Error("Failed to fetch lessons");
    }

    course.value = await courseResponse.json();
    lessons.value = await lessonsResponse.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const selectLesson = (lesson) => {
  selectedLesson.value = lesson;
};

onMounted(() => {
  fetchCourse();
});
</script>

<style scoped>
ul {
  list-style: none;
}
</style>
