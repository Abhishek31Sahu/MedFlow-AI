import { Routes, Route } from "react-router-dom";

import LaboratoryDashboard from "../pages/Laboratory/LaboratoryDashboard";

import CreateLabOrder from "../pages/Laboratory/CreateLabOrder";

import PendingLabOrders from "../pages/Laboratory/PendingLabOrders";

import PatientLabOrders from "../pages/Laboratory/PatientLabOrders";

import SubmitLabResults from "../pages/Laboratory/SubmitLabResults";

import LabReport from "../pages/Laboratory/LabReport";

import PatientReports from "../pages/Laboratory/PatientReports";

import FHIRPendingOrders from "../pages/Laboratory/FHIRPendingOrders";

export default function LaboratoryRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LaboratoryDashboard />} />

      <Route path="/orders/create" element={<CreateLabOrder />} />

      <Route path="/orders/pending" element={<PendingLabOrders />} />

      <Route path="/orders/patient/:patientId" element={<PatientLabOrders />} />

      <Route path="/results/:serviceRequestId" element={<SubmitLabResults />} />

      <Route path="/reports/:reportId" element={<LabReport />} />

      <Route path="/reports" element={<PatientReports />} />

      <Route
        path="/reports/service-request/:serviceRequestId"
        element={<PatientReports />}
      />

      <Route path="/fhir/pending" element={<FHIRPendingOrders />} />
    </Routes>
  );
}
