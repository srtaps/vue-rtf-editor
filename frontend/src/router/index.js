import AuthCard from "@/components/AuthCard.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/register",
      name: "Register",
      component: AuthCard,
      props: { formType: "register" },
    },
    {
      path: "/login",
      name: "Login",
      component: AuthCard,
      props: { formType: "login" },
    },
  ],
});

export default router;
