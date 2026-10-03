import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./routes/ProtectedRoute";

import StaffManagement from "./pages/StaffManagement";
import StaffScheduleManagement from "./pages/StaffScheduleManagement";

import BedDashboard from "./pages/Beds/BedDashboard";
import AddBed from "./pages/Beds/AddBed";
import EditBed from "./pages/Beds/EditBed";
import EncounterDashboard from "./pages/Encounters/EncounterDashboard";
import AIChat from "./pages/AI/AIChat";
import Unauthorized from "./pages/Unauthorized";
import LabTemplates from "./pages/laboratory/LabTemplates";
import CreateLabTemplate from "./pages/laboratory/CreateLabTemplate";
import LabTemplateDetails from "./pages/laboratory/LabTemplateDetails";
import EditLabTemplate from "./pages/laboratory/EditLabTemplate";
import LaboratoryRoutes from "./routes/LaboratoryRoutes";

import PatientDashboard from "./pages/Patients/PatientDashboard";
import PatientDetails from "./pages/Patients/PatientDetails";

import MedicationOverview from "./pages/medicarion/MedicationOverview";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ==================================================
            LOGIN
        ================================================== */}

        <Route path="/login" element={<Login />} />

        {/* ==================================================
            DASHBOARD
            All authenticated users
        ================================================== */}

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute
              allowedRoles={[
                "admin",
                "doctor",
                "nurse",
                "receptionist",
                "lab_technician",
                "pharmacist",
              ]}
            >
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* ==================================================
            STAFF MANAGEMENT
            Admin only
        ================================================== */}

        <Route
          path="/staff"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <StaffManagement />
            </ProtectedRoute>
          }
        />
        <Route
          path="/staff/:staffId/schedule"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <StaffScheduleManagement />
            </ProtectedRoute>
          }
        />

        {/* ==================================================
            BEDS
            Admin + Doctor + Nurse + Receptionist
        ================================================== */}

        <Route
          path="/beds"
          element={
            <ProtectedRoute
              allowedRoles={["admin", "doctor", "nurse", "receptionist"]}
            >
              <BedDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/beds/add"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <AddBed />
            </ProtectedRoute>
          }
        />

        <Route
          path="/beds/:id/edit"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <EditBed />
            </ProtectedRoute>
          }
        />

        {/* ==================================================
            AI CHAT
            Admin + Doctor
        ================================================== */}

        <Route
          path="/ai"
          element={
            <ProtectedRoute
              allowedRoles={[
                "admin",
                "doctor",
                "nurse",
                "lab_technician",
                "pharmacist",
                "receptionist",
              ]}
            >
              <AIChat />
            </ProtectedRoute>
          }
        />

        {/* ==================================================
            LABORATORY
            Admin + Doctor + Lab Technician
        ================================================== */}

        <Route
          path="/laboratory/*"
          element={
            <ProtectedRoute
              allowedRoles={["admin", "doctor", "lab_technician"]}
            >
              <LaboratoryRoutes />
            </ProtectedRoute>
          }
        />

        {/* ==================================================
            LABORATORY TEMPLATES
            Admin + Lab Technician
        ================================================== */}

        <Route
          path="/laboratory/templates"
          element={
            <ProtectedRoute allowedRoles={["admin", "lab_technician"]}>
              <LabTemplates />
            </ProtectedRoute>
          }
        />

        <Route
          path="/laboratory/templates/create"
          element={
            <ProtectedRoute allowedRoles={["admin", "lab_technician"]}>
              <CreateLabTemplate />
            </ProtectedRoute>
          }
        />

        <Route
          path="/laboratory/templates/:id"
          element={
            <ProtectedRoute
              allowedRoles={["admin", "doctor", "lab_technician"]}
            >
              <LabTemplateDetails />
            </ProtectedRoute>
          }
        />

        <Route
          path="/laboratory/templates/:id/edit"
          element={
            <ProtectedRoute allowedRoles={["admin", "lab_technician"]}>
              <EditLabTemplate />
            </ProtectedRoute>
          }
        />

        {/* ==================================================
            PATIENTS
            All authenticated hospital roles
        ================================================== */}

        <Route
          path="/patients"
          element={
            <ProtectedRoute
              allowedRoles={[
                "admin",
                "doctor",
                "nurse",
                "receptionist",
                "lab_technician",
                "pharmacist",
              ]}
            >
              <PatientDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/patients/:patientId"
          element={
            <ProtectedRoute
              allowedRoles={[
                "admin",
                "doctor",
                "nurse",
                "receptionist",
                "lab_technician",
                "pharmacist",
              ]}
            >
              <PatientDetails />
            </ProtectedRoute>
          }
        />

        {/* ==================================================
            MEDICATIONS
            Admin + Doctor + Nurse + Pharmacist
        ================================================== */}

        <Route
          path="/medications"
          element={
            <ProtectedRoute
              allowedRoles={["admin", "doctor", "nurse", "pharmacist"]}
            >
              <MedicationOverview />
            </ProtectedRoute>
          }
        />
        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route
          path="*"
          element={
            <ProtectedRoute
              allowedRoles={["admin", "doctor", "nurse", "receptionist"]}
            >
              <EncounterDashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
