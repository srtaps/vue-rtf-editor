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

const router = useRouter();
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
      throw new Error(`Status: ${response.status}`);
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

const editUser = (userId) => {
  router.push({
    name: "EditUser",
    query: { userId },
  });
};

const deleteUser = async (userId) => {
  if (confirm(`Delete user ID: ${userId}?`)) {
    try {
      const response = await fetch(`http://localhost:5000/users/${userId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      fetchUsers();
    } catch (err) {
      console.error("Error deleting user:", err);
    }
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
  background-color: #47447a50;
}

.button--edit {
  margin-right: 32px;
  background-color: #5f7ec6;
  border-radius: 8px;
}

.button--edit:hover {
  background-color: #4165b8;
}

.button--delete {
  border-radius: 8px;
  background-color: #c65f63;
}

.button--delete:hover {
  background-color: #b84146;
}
</style>
