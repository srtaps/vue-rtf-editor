<template>
  <form @submit="loginSubmit" class="form" id="login-form">
    <label for="email">Email</label>
    <input v-model="email" type="email" id="email" name="email" required />
    <label for="password">Password</label>
    <input
      v-model="password"
      type="password"
      id="password"
      name="password"
      required
    />
    <button class="button--submit" type="submit" :disabled="isLoading">
      {{ isLoading ? "Logging in..." : "Log in" }}
    </button>
  </form>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const email = ref("");
const password = ref("");
const isLoading = ref(false);

const loginSubmit = async (event) => {
  event.preventDefault();
  isLoading.value = true;

  try {
    const response = await fetch(`http://127.0.0.1:5000/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email: email.value, password: password.value }),
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("access_token", data.access_token);

      email.value = "";
      password.value = "";

      router.push("/home");
    } else {
      console.log(data.error);
    }
  } catch (err) {
    console.error("Login error:", err.message);
  } finally {
    isLoading.value = false;
  }
};
</script>
