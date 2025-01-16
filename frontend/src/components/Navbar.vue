<template>
  <nav class="navigation">
    <div class="navigation__logo">Placeholder</div>
    <div class="navigation__links">
      <ul class="link__list">
        <li><a href="/home">Home</a></li>
        <li><a href="#">Administraion</a></li>
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
  padding: 16px 24px;
  display: flex;
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
  transition: text-decoration 0.3s ease;
}

.link__list a:hover {
  color: #1c96b6;
  text-decoration: underline;
}
</style>
