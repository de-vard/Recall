import React from "react";
import { Routes, Route } from "react-router-dom";

import Home from "./components/Home";

import ProtectedRoute from "./components/layout/ProtectedRoute";
import Layout from "./components/layout/Layout";
import UnderConstructionSculptor from "./components/UnderConstructionSculptor";

import Registration from "./components/auth/Registration";
import Login from "./components/auth/Login";

import CourseDetail from "./components/courses/CourseDetail";
import CourseEdit from "./components/courses/CourseEdit";
import CourseDelete from "./components/courses/CourseDelete";
import CourseCreate from "./components/courses/CourseCreate";
import CourseList from "./components/courses/CourseList";
import CourseMy from "./components/courses/CourseMy";

import FolderDetail from "./components/folders/FolderDetail";
import FolderEdit from "./components/folders/FolderEdit";
import FolderCreate from "./components/folders/FolderCreate";
import FolderDelete from "./components/folders/FolderDelete";

import ModuleDetail from "./components/modules/ModuleDetail";
import ModuleCreate from "./components/modules/ModuleCreate";
import ModuleDelete from "./components/modules/ModuleDelete";
import ModuleEdit from "./components/modules/ModuleEdit";

import StudyDetail from "./components/study/StudyDetail";
import StudyHistory from "./components/study/StudyHistory";



function App() {
  return (
    <Routes>
      <Route path="/register/" element={<Registration />} />
      <Route path="/login/" element={<Login />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />

          {/* Заглушка компонента для нереализованных страниц */}
          <Route path="/coming-soon" element={<UnderConstructionSculptor />} />

          <Route path="study/:public_id" element={<StudyDetail />} />
          <Route path="history/:public_id" element={<StudyHistory />} />

          <Route path="module/:public_id" element={<ModuleDetail />} />
          <Route path="module/create/:public_id" element={<ModuleCreate />} />
          <Route path="module/delete/:public_id" element={<ModuleDelete />} />
          <Route path="module/edit/:public_id" element={<ModuleEdit />} />

          <Route path="course/" element={<CourseList />} />
          <Route path="course/my" element={<CourseMy />} />
          <Route path="course/:public_id" element={<CourseDetail />} />
          <Route path="course/create/:public_id" element={<CourseCreate />} />
          <Route path="course/edit/:public_id" element={<CourseEdit />} />
          <Route path="course/delete/:public_id" element={<CourseDelete />} />

          <Route path="folder/:public_id" element={<FolderDetail />} />
          <Route path="folder/edit/:public_id" element={<FolderEdit />} />
          <Route path="folder/create/:public_id" element={<FolderCreate />} />
          <Route path="folder/delete/:public_id" element={<FolderDelete />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
