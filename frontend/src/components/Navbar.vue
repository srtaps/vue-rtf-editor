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
      </ul>
      <button @click="handleLogout" class="button button--logout">
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const handleLogout = () => {
  localStorage.removeItem("access_token");
  router.push("/login");
};
</script>

<style scoped></style>
