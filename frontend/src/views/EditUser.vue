<template>
  <div class="vue-views" id="edit-user">
    <Navbar />
    <div class="vue-views__container">
      <h2>Edit user</h2>

      <div v-if="loading" class="mt-16">Loading user data...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <form
        v-if="!loading && !error"
        @submit.prevent="editSubmit"
        class="form mt-32"
        id="edit-form"
      >
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

        <label for="role">Role:</label>
        <select id="role" v-model="roleId" required>
          <option
            v-for="role in roles"
            :key="role.role_id"
            :value="role.role_id"
          >
            {{ role.role_name }}
          </option>
        </select>

        <button class="button button--submit mt-32" type="submit">Save</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { toast } from "vue3-toastify";

const router = useRouter();
const route = useRoute();
const userId = route.query.userId;

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const roles = ref([]);
const roleId = ref("");

const loading = ref(true);
const error = ref(null);

const fetchUser = async () => {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(`http://localhost:5000/users/${userId}`, {
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

    firstName.value = data.first_name;
    lastName.value = data.last_name;
    email.value = data.email;
    roleId.value = data.role_id;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const fetchRoles = async () => {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch("http://localhost:5000/roles", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(data.msg || data.error);
    }

    roles.value = await response.json();
  } catch (err) {
    error.value = err.message;
  }
};

const editSubmit = async () => {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(`http://localhost:5000/users/${userId}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        first_name: firstName.value,
        last_name: lastName.value,
        email: email.value,
        role_id: roleId.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.msg || data.error);
    }

    router.push("/users").then(() => toast.success(data.message));
  } catch (err) {
    error.value = err.message;
    toast.error(err.message);
  }
};

onMounted(() => {
  fetchUser();
  fetchRoles();
});
</script>

<style scoped></style>
