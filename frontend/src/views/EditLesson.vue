<template>
  <div class="vue-views" id="edit-lesson">
    <Navbar />
    <div class="vue-views__container">
      <h2>{{ isEditing ? "Edit lesson" : "Add lesson" }}</h2>

      <div v-if="loading" class="mt-16">Loading lesson data...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <form
        v-if="!loading && !error"
        @submit.prevent="handleSubmit"
        class="form mt-32"
        id="edit-form"
      >
        <label for="lesson-title">Title</label>
        <input
          v-model="title"
          type="text"
          id="lesson-title"
          name="title"
          required
        />

        <label for="course-name">Course Name</label>
        <select id="course-name" v-model="courseId">
          <option
            v-for="course in courses"
            :key="course.course_id"
            :value="course.course_id"
          >
            {{ course.title }}
          </option>
        </select>

        <Editor ref="editorRef" @editor-ready="setContent" class="mt-32" />

        <button class="button button--submit mt-32" type="submit">
          {{ isEditing ? "Update" : "Add" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import Editor from "@/components/Editor.vue";
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();

const isEditing = computed(() => !!route.query.lessonId);
const lessonId = route.query.lessonId;
const loading = ref(true);
const error = ref(null);

const title = ref("");
const courses = ref([]);
const courseId = ref("");
const editorRef = ref(null);
let editorData = ``;

const fetchLesson = async () => {
  if (isEditing.value) {
    try {
      const response = await fetch(`http://localhost:5000/lessons/${lessonId}`);

      if (!response.ok) {
        throw new Error("Failed to fetch lesson");
      }

      const data = await response.json();

      title.value = data.title;
      courseId.value = data.course_id;
      editorData = data.content;
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  } else {
    loading.value = false;
  }
};

const fetchCourses = async () => {
  try {
    const response = await fetch("http://localhost:5000/courses");

    if (!response.ok) {
      throw new Error("Failed to fetch courses");
    }

    courses.value = await response.json();
  } catch (err) {
    error.value = err.message;
  }
};

const handleSubmit = async () => {
  // const url = isEditing.value ? `lessons/${route.query.lessonId}` : "lessons";
  // const method = isEditing.value ? "PUT" : "POST";
  // content = getContent();
  //
  // try {
  //   const response = await fetch(`http://localhost:5000/${url}`, {
  //     method,
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //     body: JSON.stringify({
  //       title: title.value,
  //       content: content,
  //       course_id: courseId.value,
  //     }),
  //   });
  //   if (!response.ok) {
  //     throw new Error("Failed to update lesson");
  //   }
  //   router.push("/lessons");
  // } catch (err) {
  //   error.value = err.message;
  // }
};

function getContent() {
  return editorRef.value.getEditorContent();
}

function setContent() {
  editorRef.value.setEditorContent(editorData);
}

onMounted(() => {
  fetchLesson();
  fetchCourses();
});
</script>
