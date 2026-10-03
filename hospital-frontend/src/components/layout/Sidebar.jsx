import { NavLink } from "react-router-dom";

import {
  FaHospital,
  FaTachometerAlt,
  FaUserInjured,
  FaProcedures,
  FaCalendarAlt,
  FaFlask,
  FaBed,
  FaPills,
  FaUsersCog,
  FaChartBar,
  FaCog,
  FaShieldAlt,
  FaRobot,
} from "react-icons/fa";

// ==========================================================
// MENU ITEMS
// ==========================================================

const menuItems = [
  {
    key: "dashboard",
    title: "Dashboard",
    icon: <FaTachometerAlt />,
    path: "/dashboard",
  },
  {
    key: "aiChat",
    title: "AI Chat",
    icon: <FaRobot />,
    path: "/ai",
  },
  {
    key: "patients",
    title: "Patients",
    icon: <FaUserInjured />,
    path: "/patients",
  },
  {
    key: "encounters",
    title: "Encounters",
    icon: <FaProcedures />,
    path: "/encounters",
  },
  {
    key: "appointments",
    title: "Appointments",
    icon: <FaCalendarAlt />,
    path: "/appointments",
  },
  {
    key: "laboratory",
    title: "Laboratory",
    icon: <FaFlask />,
    path: "/laboratory",
  },
  {
    key: "labTemplates",
    title: "Laboratory Templates",
    icon: <FaFlask />,
    path: "/laboratory/templates",
  },
  {
    key: "beds",
    title: "Beds",
    icon: <FaBed />,
    path: "/beds",
  },
  {
    key: "medications",
    title: "Medications",
    icon: <FaPills />,
    path: "/medications",
  },
  {
    key: "staff",
    title: "Staff Management",
    icon: <FaUsersCog />,
    path: "/staff",
  },
  {
    key: "reports",
    title: "Reports",
    icon: <FaChartBar />,
    path: "/reports",
  },
  {
    key: "settings",
    title: "Settings",
    icon: <FaCog />,
    path: "/settings",
  },
];

// ==========================================================
// ROLE PERMISSIONS
// ==========================================================

const rolePermissions = {
  admin: [
    "dashboard",
    "aiChat",
    "patients",
    "encounters",
    "appointments",
    "laboratory",
    "labTemplates",
    "beds",
    "medications",
    "staff",
    "reports",
    "settings",
  ],

  doctor: [
    "dashboard",
    "aiChat",
    "patients",
    "encounters",
    "appointments",
    "laboratory",
    "beds",
    "medications",
    "reports",
  ],

  nurse: [
    "dashboard",
    "aiChat",
    "patients",
    "encounters",
    "appointments",
    "beds",
    "medications",
    "reports",
  ],

  receptionist: [
    "dashboard",
    "aiChat",
    "patients",
    "encounters",
    "appointments",
  ],

  lab_technician: [
    "dashboard",
    "aiChat",
    "patients",
    "laboratory",
    "labTemplates",
    "reports",
  ],

  pharmacist: ["dashboard", "aiChat", "patients", "medications", "reports"],
};

// ==========================================================
// ROLE DISPLAY NAMES
// ==========================================================

const roleDisplayNames = {
  admin: "Administrator",
  doctor: "Doctor",
  nurse: "Nurse",
  receptionist: "Receptionist",
  lab_technician: "Lab Technician",
  pharmacist: "Pharmacist",
};

// ==========================================================
// SIDEBAR
// ==========================================================

export default function Sidebar() {
  // --------------------------------------------------------
  // Get logged-in user
  // --------------------------------------------------------

  const storedUser = localStorage.getItem("user");

  let user = null;

  try {
    user = storedUser ? JSON.parse(storedUser) : null;
  } catch (error) {
    console.error("Failed to parse logged-in user:", error);
  }

  // --------------------------------------------------------
  // Get role
  // --------------------------------------------------------

  const role = user?.role?.toLowerCase();

  const allowedItems = rolePermissions[role] || [];

  // --------------------------------------------------------
  // Filter navigation
  // --------------------------------------------------------

  const visibleMenuItems = menuItems.filter((item) =>
    allowedItems.includes(item.key),
  );

  // --------------------------------------------------------
  // User information
  // --------------------------------------------------------

  const fullName =
    [user?.first_name, user?.last_name].filter(Boolean).join(" ") ||
    user?.username ||
    "User";

  const roleName = roleDisplayNames[role] || "User";

  // ========================================================
  // UI
  // ========================================================

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-gradient-to-b from-blue-800 to-blue-900 text-white shadow-xl flex flex-col">
      {/* ==================================================
          Logo
      ================================================== */}

      <div className="flex items-center gap-3 p-6 border-b border-blue-700">
        <div className="bg-white text-blue-700 rounded-full p-3 text-3xl">
          <FaHospital />
        </div>

        <div>
          <h1 className="text-xl font-bold">AI Hospital</h1>

          <p className="text-sm text-blue-200">Workflow System</p>
        </div>
      </div>

      {/* ==================================================
          Navigation
      ================================================== */}

      <div className="sidebar-scroll flex-1 overflow-y-auto py-5">
        <div className="flex-1 overflow-y-auto py-5">
          {visibleMenuItems.map((item) => (
            <NavLink
              key={item.key}
              to={item.path}
              className={({ isActive }) =>
                `mx-3 mb-2 flex items-center gap-4 rounded-xl px-5 py-3 transition-all duration-300
                ${isActive ? "bg-blue-600 shadow-lg" : "hover:bg-blue-700"}`
              }
            >
              <span className="text-xl">{item.icon}</span>

              <span className="font-medium">{item.title}</span>
            </NavLink>
          ))}
        </div>
      </div>

      {/* ==================================================
          Footer / Current User
      ================================================== */}

      <div className="border-t border-blue-700 p-4">
        <div className="flex items-center gap-3 rounded-xl bg-blue-800 p-4">
          <div className="rounded-full bg-white p-3 text-blue-700">
            <FaShieldAlt />
          </div>

          <div className="min-w-0">
            <h3 className="font-semibold truncate">{fullName}</h3>

            <p className="text-sm text-blue-200 truncate">{roleName}</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
