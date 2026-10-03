import { Card, CardContent } from "@mui/material";

export default function StatCard({
  title,
  value,
  icon,
  color = "bg-blue-600",
  change,
  changeType = "positive",
}) {
  return (
    <Card className="rounded-2xl shadow-md hover:shadow-xl transition-all duration-300">
      <CardContent className="flex items-center justify-between p-6">
        {/* Left */}

        <div>
          <p className="text-gray-500 text-sm font-medium">{title}</p>

          <h2 className="text-3xl font-bold mt-2">{value}</h2>

          {change && (
            <div
              className={`mt-3 inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold
              ${
                changeType === "positive"
                  ? "bg-green-100 text-green-700"
                  : "bg-red-100 text-red-700"
              }`}
            >
              {change}
            </div>
          )}
        </div>

        {/* Icon */}

        <div
          className={`${color} h-16 w-16 rounded-2xl flex items-center justify-center text-white text-3xl shadow-lg`}
        >
          {icon}
        </div>
      </CardContent>
    </Card>
  );
}
