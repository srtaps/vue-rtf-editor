<template>
  <div class="vue-views" id="course-content">
    <Navbar />
    <div class="vue-views__container">
      <div v-if="loading" class="mt-16">Loading lesson...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <div v-if="!loading && !error" class="lesson__grid">
        <div class="lesson__nav">
          <p class="text-bold">{{ course.title }}</p>
          <ul class="mt-16">
            <li v-for="lesson in lessons" :key="lesson.lesson_id">
              <p
                @click="selectLesson(lesson)"
                class="lesson__link"
                :class="{
                  'selected-lesson': selectedLesson?.title === lesson.title,
                }"
              >
                {{ lesson.title }}
              </p>
            </li>
          </ul>
        </div>
        <div class="lesson__content" v-if="selectedLesson">
          <h2>{{ selectedLesson.title }}</h2>
          <div v-html="selectedLesson.content" class="mt-32"></div>
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
const selectedLesson = ref({
  lesson_id: null,
});
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
  // console.log("Lesson object:", lesson);
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

.lesson__grid {
  display: grid;
  grid-template-columns: 1fr 3fr;
  gap: 24px;
}

.lesson__nav {
  background-color: #272734;
  padding: 12px;
  border-radius: 8px;
}

.lesson__link {
  cursor: pointer;
  margin-top: 8px;
  padding: 4px 8px;
  border-radius: 8px;
}

.lesson__link:hover {
  background-color: #7874cd;
}

.selected-lesson {
  border-left: 4px solid #453fb1;
  border-radius: 4px;
  font-weight: 600;
}
</style>
