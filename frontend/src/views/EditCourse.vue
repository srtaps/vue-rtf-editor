<template>
  <div class="vue-views" id="edit-course">
    <Navbar />
    <div class="vue-views__container">
      <h2>{{ isEditing ? "Edit course" : "Create course" }}</h2>

      <div v-if="loading" class="mt-16">Loading course data...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <form
        v-if="!loading && !error"
        @submit.prevent="handleSubmit"
        class="form mt-32"
        id="edit-form"
      >
        <label for="course-title">Title</label>
        <input
          v-model="title"
          type="text"
          id="course-title"
          name="title"
          required
        />
        <label for="course-info">Info</label>
        <textarea
          v-model="info"
          id="course-info"
          name="info"
          required
        ></textarea>
        <label for="course-professor">Professor</label>
        <input
          v-model="professor"
          type="text"
          id="course-professor"
          name="professor"
          required
        />

        <button class="button button--submit mt-32" type="submit">
          {{ isEditing ? "Update" : "Create" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { toast } from "vue3-toastify";

const router = useRouter();
const route = useRoute();
const courseId = route.query.courseId;

const isEditing = computed(() => !!route.query.courseId);

const title = ref("");
const info = ref("");
const professor = ref("");

const loading = ref(true);
const error = ref(null);

const fetchCourse = async () => {
  if (isEditing.value) {
    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch(
        `http://localhost:5000/courses/${courseId}`,
        {
          method: "GET",
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

      title.value = data.title;
      info.value = data.info;
      professor.value = data.professor;
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  } else {
    loading.value = false;
  }
};

const handleSubmit = async () => {
  const url = isEditing.value ? `courses/${route.query.courseId}` : "courses";
  const method = isEditing.value ? "PUT" : "POST";

  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(`http://localhost:5000/${url}`, {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: title.value,
        info: info.value,
        professor: professor.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.msg || data.error);
    }

    router.push("/courses").then(() => toast.success(data.message));
  } catch (err) {
    error.value = err.message;
    toast.error(err.message);
  }
};

onMounted(() => {
  fetchCourse();
});
</script>

<style scoped></style>
