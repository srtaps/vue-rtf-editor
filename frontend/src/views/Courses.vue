<template>
  <div class="vue-views" id="courses">
    <Navbar />
    <div class="vue-views__container">
      <h2>Courses</h2>

      <div v-if="loading" class="mt-16">Loading courses...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <div v-if="!loading && !error" class="">
        <button @click="addCourse()" class="button button--add mt-32">
          Add course
        </button>

        <table class="">
          <thead>
            <tr>
              <th>Course ID</th>
              <th>Title</th>
              <th>Info</th>
              <th>Professor</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in courses" :key="course.course_id">
              <td>{{ course.course_id }}</td>
              <td>{{ course.title }}</td>
              <td class="column-info">{{ course.info }}</td>
              <td>{{ course.professor }}</td>
              <td>
                <button
                  @click="editCourse(course.course_id)"
                  class="button button--edit"
                >
                  Edit
                </button>
                <button
                  @click="deleteCourse(course.course_id)"
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
const courses = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchCourses = async () => {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch("http://localhost:5000/courses", {
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

    courses.value = data;
  } catch (err) {
    console.error("Error fetching courses:", err);
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const editCourse = (courseId) => {
  router.push({
    name: "EditCourse",
    query: { courseId },
  });
};

const addCourse = () => {
  router.push({
    name: "EditCourse",
  });
};

const deleteCourse = async (courseId) => {
  if (confirm(`Delete course ID: ${courseId}?`)) {
    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch(
        `http://localhost:5000/courses/${courseId}`,
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
      fetchCourses();
    } catch (err) {
      console.error("Error deleting course:", err);
      toast.error(err.message);
    }
  }
};

onMounted(() => {
  fetchCourses();
});
</script>

<style scoped></style>
