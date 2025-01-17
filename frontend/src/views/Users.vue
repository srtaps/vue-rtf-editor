<template>
  <div class="vue-views" id="users">
    <Navbar />
    <div class="vue-views__container">
      <h2>Users</h2>

      <div v-if="loading" class="status-message">Loading users...</div>

      <div v-if="error" class="status-message">Error: {{ error }}</div>

      <div v-if="!loading && !error" class="">
        <table class="">
          <thead>
            <tr>
              <th class="">Full Name</th>
              <th class="">Email</th>
              <th class="">Role</th>
              <th class="">Created At</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.user_id">
              <td class="">{{ user.full_name }}</td>
              <td class="">{{ user.email }}</td>
              <td class="">{{ user.role_name }}</td>
              <td class="">
                {{ new Date(user.created_at).toLocaleDateString() }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Navbar from "@/components/Navbar.vue";

const users = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchUsers = async () => {
  try {
    const response = await fetch("http://localhost:5000/users", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Error, status: ${response.status}`);
    }

    const data = await response.json();
    users.value = data;
  } catch (err) {
    console.error("Error fetching users:", err);
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 24px;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #555555;
}

th {
  background-color: #645fc6;
  font-weight: bold;
}

tr:hover {
  background-color: #47447a;
}
</style>
