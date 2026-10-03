import { Link } from "react-router-dom";

export default function Unauthorized() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white rounded-2xl shadow-lg p-10 text-center">
        <h1 className="text-4xl font-bold text-red-600">403</h1>

        <h2 className="text-2xl font-semibold mt-3">Access Denied</h2>

        <p className="text-gray-600 mt-2">
          You do not have permission to access this page.
        </p>

        <Link
          to="/dashboard"
          className="inline-block mt-6 px-5 py-3 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
        >
          Go to Dashboard
        </Link>
      </div>
    </div>
  );
}
