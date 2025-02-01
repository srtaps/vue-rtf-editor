<template>
  <nav class="navigation">
    <div class="navigation__logo">VueCourse</div>
    <div class="navigation__links">
      <ul class="link__list">
        <li>
          <router-link to="/home" active-class="active-link">
            Home
          </router-link>
        </li>
        <template v-if="userRole === 'Admin'">
          <li>
            <router-link to="/users" active-class="active-link"
              >Users
            </router-link>
          </li>
          <li>
            <router-link to="/courses" active-class="active-link"
              >Courses
            </router-link>
          </li>
          <li>
            <router-link to="/lessons" active-class="active-link"
              >Lessons
            </router-link>
          </li>
        </template>
      </ul>
      <button @click="handleLogout" class="button button--logout">
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";

const router = useRouter();
const userRole = ref("");

const handleLogout = () => {
  localStorage.removeItem("access_token");
  router.push("/login").then(() => toast.success("Logged out"));
};

onMounted(() => {
  userRole.value = localStorage.getItem("user_role");
});
</script>

<style scoped></style>
