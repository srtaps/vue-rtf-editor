<template>
  <div class="vue-views" id="users">
    <Navbar />
    <div class="vue-views__container">
      <h2>Users</h2>

      <div v-if="loading" class="mt-16">Loading users...</div>
      <div v-if="error" class="mt-16">Error: {{ error }}</div>

      <div v-if="!loading && !error" class="">
        <table class="">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.user_id">
              <td>{{ user.user_id }}</td>
              <td>{{ user.full_name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.role_name }}</td>
              <td>
                {{ new Date(user.created_at).toLocaleDateString() }}
              </td>
              <td>
                <button
                  @click="editUser(user.user_id)"
                  class="button button--edit"
                >
                  Edit
                </button>
                <button
                  @click="deleteUser(user.user_id)"
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
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Navbar from "@/components/Navbar.vue";
import { toast } from "vue3-toastify";

const router = useRouter();
const users = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchUsers = async () => {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch("http://localhost:5000/users", {
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

    users.value = data;
  } catch (err) {
    console.error("Error fetching users:", err);
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const editUser = (userId) => {
  router.push({
    name: "EditUser",
    query: { userId },
  });
};

const deleteUser = async (userId) => {
  if (confirm(`Delete user ID: ${userId}?`)) {
    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch(`http://localhost:5000/users/${userId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.msg || data.error);
      }

      toast.success(data.message);
      fetchUsers();
    } catch (err) {
      console.error("Error deleting user:", err);
      toast.error(err.message);
    }
  }
};

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped></style>
