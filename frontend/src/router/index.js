import { createRouter, createWebHistory } from "vue-router";
import AuthCard from "@/components/AuthCard.vue";
import Home from "@/views/Home.vue";
import Users from "@/views/Users.vue";
import EditUser from "@/views/EditUser.vue";
import Courses from "@/views/Courses.vue";
import EditCourse from "@/views/EditCourse.vue";
import Lessons from "@/views/Lessons.vue";
import EditLesson from "@/views/EditLesson.vue";

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
    {
      path: "/courses",
      name: "Courses",
      component: Courses,
      meta: { requiresAuth: true },
    },
    {
      path: "/courses/edit",
      name: "EditCourse",
      component: EditCourse,
      meta: { requiresAuth: true },
    },
    {
      path: "/lessons",
      name: "Lessons",
      component: Lessons,
      meta: { requiresAuth: true },
    },
    {
      path: "/lessons/edit",
      name: "EditLesson",
      component: EditLesson,
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
