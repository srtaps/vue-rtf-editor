<template>
  <div class="auth-card">
    <div class="container">
      <div class="auth-card__left">
        <h2 class="auth-card__title">{{ heading }}</h2>
        <p v-if="formType === 'register'">
          Already have an account?<br /><a href="/login"
            >Click here to log in</a
          >
        </p>
        <p v-else>
          Don't have an account?<br /><a href="/register"
            >Click here to sign up</a
          >
        </p>
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
      return this.formType === "register"
        ? "Join our community"
        : "Welcome to VueLearn";
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
