<template>
  <nav class="navigation">
    <div class="navigation__logo">Placeholder</div>
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

<style scoped>
.navigation {
  background-color: #2c2c38;
  font-size: 1.1rem;
  padding: 16px 32px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.navigation__logo {
  margin: auto 0;
}

.navigation__links {
  display: flex;
  gap: 24px;
}

.link__list {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 16px;
}

.link__list a {
  text-decoration: none;
}

.link__list a:hover {
  color: #1c96b6;
  text-decoration: underline;
}

.active-link {
  font-weight: bold;
  color: #4ad0e3;
}

a.active-link {
  text-decoration: underline;
}
</style>
