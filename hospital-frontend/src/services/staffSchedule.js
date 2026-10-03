import api from "../api/axios";

/**
 * CREATE
 * POST /practitioner-schedules/
 */
export const createPractitionerSchedule = async (data) => {
  const response = await api.post("/practitioner-schedules/", data);

  return response.data;
};

/**
 * GET ALL SCHEDULES FOR PRACTITIONER
 * GET /practitioner-schedules/practitioner/{practitioner_id}
 */
export const getPractitionerSchedules = async (practitionerId) => {
  const response = await api.get(
    `/practitioner-schedules/practitioner/${practitionerId}`,
  );

  return response.data;
};

/**
 * GET SCHEDULE FOR PARTICULAR DAY
 * GET /practitioner-schedules/practitioner/{practitioner_id}/day/{day_of_week}
 */
export const getPractitionerScheduleForDay = async (
  practitionerId,
  dayOfWeek,
) => {
  const response = await api.get(
    `/practitioner-schedules/practitioner/${practitionerId}/day/${dayOfWeek}`,
  );

  return response.data;
};

/**
 * GET TODAY'S SCHEDULE
 * GET /practitioner-schedules/practitioner/{practitioner_id}/today
 */
export const getTodaySchedule = async (practitionerId) => {
  const response = await api.get(
    `/practitioner-schedules/practitioner/${practitionerId}/today`,
  );

  return response.data;
};

/**
 * CHECK WHETHER PRACTITIONER IS WORKING TODAY
 * GET /practitioner-schedules/practitioner/{practitioner_id}/working-today
 */
export const isPractitionerWorkingToday = async (practitionerId) => {
  const response = await api.get(
    `/practitioner-schedules/practitioner/${practitionerId}/working-today`,
  );

  return response.data;
};

/**
 * UPDATE
 * PUT /practitioner-schedules/{schedule_id}
 */
export const updatePractitionerSchedule = async (scheduleId, data) => {
  const response = await api.put(`/practitioner-schedules/${scheduleId}`, data);

  return response.data;
};

/**
 * DELETE
 * DELETE /practitioner-schedules/{schedule_id}
 */
export const deletePractitionerSchedule = async (scheduleId) => {
  const response = await api.delete(`/practitioner-schedules/${scheduleId}`);

  return response.data;
};
