import { createRouter, createWebHistory } from "vue-router";
import AuthCard from "@/components/AuthCard.vue";
import Home from "@/views/Home.vue";
import LessonEditor from "@/views/LessonEditor.vue";
import Users from "@/views/Users.vue";
import EditUser from "@/views/EditUser.vue";

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
    {
      path: "/home",
      name: "Home",
      component: Home,
      meta: { requiresAuth: true },
    },
    {
      path: "/new-lesson",
      name: "Editor",
      component: LessonEditor,
      meta: { requiresAuth: true },
    },
    {
      path: "/users",
      name: "Users",
      component: Users,
      meta: { requiresAuth: true },
    },
    {
      path: "/users/edit",
      name: "EditUser",
      component: EditUser,
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  if (to.meta.requiresAuth && !token) {
    next("/login");
    return;
  } else if ((to.name === "Login" || to.name === "Register") && token) {
    next("/home");
    return;
  } else if (to.path === "/") {
    next("/login");
    return;
  }

  next();
});

export default router;
