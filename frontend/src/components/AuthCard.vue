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

<script setup>
// Import defineAsyncComponent to handle async component loading
import { computed, defineAsyncComponent } from "vue";

const props = defineProps({
  formType: {
    type: String,
    required: true,
  },
});

const heading = computed(() =>
  props.formType === "register" ? "Join our community" : "Welcome to VueLearn"
);

const formComponent = computed(() =>
  props.formType === "register"
    ? defineAsyncComponent(() => import("@/components/RegisterForm.vue"))
    : defineAsyncComponent(() => import("@/components/LoginForm.vue"))
);
</script>

<style scoped></style>
