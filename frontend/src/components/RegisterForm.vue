<template>
  <form @submit="registerSubmit" class="form" id="register-form">
    <label for="first-name">First name</label>
    <input
      v-model="firstName"
      type="text"
      id="first-name"
      name="firstName"
      required
    />
    <label for="last-name">Last name</label>
    <input
      v-model="lastName"
      type="text"
      id="last-name"
      name="lastName"
      required
    />
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
    <button class="button button--submit" type="submit" :disabled="isLoading">
      {{ isLoading ? "Registering..." : "Register" }}
    </button>
  </form>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";

const router = useRouter();
const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");
const isLoading = ref(false);

const registerSubmit = async (event) => {
  event.preventDefault();
  isLoading.value = true;

  try {
    const response = await fetch(`http://127.0.0.1:5000/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        firstName: firstName.value.trim(),
        lastName: lastName.value.trim(),
        email: email.value.trim(),
        password: password.value.trim(),
      }),
    });

    const data = await response.json();

    if (response.ok) {
      firstName.value = "";
      lastName.value = "";
      email.value = "";
      password.value = "";

      router.push("/login").then(() => toast.success(data.message));
    } else {
      // console.log(data.error);
      toast.error(data.error);
    }
  } catch (err) {
    console.error("Register error:", err.message);
    toast.error(err.message);
  } finally {
    isLoading.value = false;
  }
};
</script>
