<template>
  <div class="vue-views" id="courses">
    <Navbar />
    <div class="vue-views__container">
      <h2>Courses</h2>

      <button @click="addCourse()" class="button button--add mt-32">
        Add course
      </button>

      <div v-if="loading" class="mt-16">Loading courses...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <div v-if="!loading && !error" class="">
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
              <td class="course-info">{{ course.info }}</td>
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

const router = useRouter();
const courses = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchCourses = async () => {
  try {
    const response = await fetch("http://localhost:5000/courses", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Status: ${response.status}`);
    }

    const data = await response.json();
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
    try {
      const response = await fetch(
        `http://localhost:5000/courses/${courseId}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      fetchCourses();
    } catch (err) {
      console.error("Error deleting course:", err);
    }
  }
};

onMounted(() => {
  fetchCourses();
});
</script>

<style scoped>
.button--add {
  background-color: #2c2c38;
  border: 2px solid #645fc6;
  text-transform: uppercase;
  font-weight: bold;
  font-size: 1.1rem;
  border-radius: 4px;
}

.button--add:hover {
  background-color: #525868;
}

.course-info {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
