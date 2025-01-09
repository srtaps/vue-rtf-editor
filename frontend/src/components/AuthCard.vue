<template>
  <div class="auth-card">
    <div class="container">
      <div class="auth-card__left">
        <h2>{{ heading }}</h2>
      </div>
      <div class="auth-card__right">
        <!-- Dynamically load the form based on the formType prop -->
        <component :is="formComponent" />
      </div>
    </div>
  </div>
</template>

<script>
// Import defineAsyncComponent to handle async component loading
import { defineAsyncComponent } from "vue";

export default {
  props: {
    formType: {
      type: String,
      required: true,
    },
  },
  computed: {
    heading() {
      return this.formType === "register" ? "Register" : "Login";
    },
    formComponent() {
      // Lazy loading components
      return this.formType === "register"
        ? defineAsyncComponent(() => import("@/components/RegisterForm.vue"))
        : defineAsyncComponent(() => import("@/components/LoginForm.vue"));
    },
  },
};
</script>

<style scoped></style>
