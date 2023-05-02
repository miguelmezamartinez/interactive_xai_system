import { createRouter, createWebHistory } from "vue-router";
import DatasetExplorer from "../views/DatasetExplorer.vue";
import InstancePage from "../views/InstancePage.vue";
import ExperimentPage from "../views/ExperimentPage.vue"
import AdminPage from "../views/AdminPage.vue"

const routes = [
  {
    path: "/",
    redirect: { name: "Dataset Explorer" }
  },
  {
    path: "/dataset",
    name: "Dataset Explorer",
    component: DatasetExplorer,
  },
  {
    path: "/applications/:id",
    name: "Application View",
    component: InstancePage,
  },
  {
    path: "/experiments/:name",
    name: "Experiment Page",
    component: ExperimentPage
  },
  {
    path: "/admin",
    name: "Admin Page",
    component: AdminPage
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
