<template>
  <div class="vue-views" id="lessons">
    <Navbar />
    <div class="vue-views__container">
      <h2>Lessons</h2>

      <div v-if="loading" class="mt-16">Loading lessons...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <div v-if="!loading && !error" class="">
        <button @click="addLesson()" class="button button--add mt-32">
          Add lesson
        </button>

        <table class="">
          <thead>
            <tr>
              <th>Lesson ID</th>
              <th>Title</th>
              <th>Content</th>
              <th>Course Name</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lesson in lessons" :key="lesson.lesson_id">
              <td>{{ lesson.lesson_id }}</td>
              <td>{{ lesson.title }}</td>
              <td class="column-info">{{ lesson.content }}</td>
              <td>{{ lesson.course_title }}</td>
              <td>
                <button
                  @click="editLesson(lesson.lesson_id)"
                  class="button button--edit"
                >
                  Edit
                </button>
                <button
                  @click="deleteLesson(lesson.lesson_id)"
                  class="button button--delete"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";

const router = useRouter();
const lessons = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchLessons = async () => {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch("http://localhost:5000/lessons", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.msg || data.error);
    }

    lessons.value = data;
  } catch (err) {
    console.error("Error fetching lessons:", err);
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const editLesson = (lessonId) => {
  router.push({
    name: "EditLesson",
    query: { lessonId },
  });
};

const addLesson = () => {
  router.push({
    name: "EditLesson",
  });
};

const deleteLesson = async (lessonId) => {
  if (confirm(`Delete lesson ID: ${lessonId}?`)) {
    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch(
        `http://localhost:5000/lessons/${lessonId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.msg || data.error);
      }

      toast.success(data.message);
      fetchLessons();
    } catch (err) {
      console.error("Error deleting lesson:", err);
      toast.error(err.message);
    }
  }
};

onMounted(() => {
  fetchLessons();
});
</script>

<style scoped></style>
