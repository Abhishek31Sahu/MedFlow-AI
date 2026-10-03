import { useState } from "react";
import aiService from "../services/aiService";

export function useChat(practitionerId) {
  const [messages, setMessages] = useState([
    {
      id: Date.now(),
      role: "assistant",
      title: "AI Hospital Assistant",
      content: "👋 Hello Doctor! How can I help you today?",
    },
  ]);

  const [loading, setLoading] = useState(false);
  const [threadId, setThreadId] = useState(null);
  const [interrupt, setInterrupt] = useState(null);

  // ==========================================================
  // Send Message
  // ==========================================================

  const sendMessage = async (query) => {
    if (!query.trim()) return;

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: query,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await aiService.chat({
        query,
        practitioner_id: practitionerId,
        thread_id: threadId,
      });

      console.log(response);

      setThreadId(response.thread_id);

      if (response.interrupt) {
        setInterrupt(response.interrupt);

        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            role: "assistant",
            title: response.interrupt.type || "Action Required",
            content:
              response.interrupt.message || "More information is required.",
            data: response.interrupt,
          },
        ]);

        return;
      }

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          // Standardized ResponseOutput from response_agent — this is
          // what MessageBubble/ResponseCard renders. Title/content/data
          // are kept alongside it only as a fallback for any code path
          // that hasn't been updated to read `.response` yet.
          response: response.response,
          title: response.response?.title || "AI Hospital Assistant",
          content:
            response.response?.message || "Operation completed successfully.",
          data: response.response?.data || null,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          title: "Error",
          content:
            error.response?.data?.detail ||
            "❌ Unable to process your request.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // Resolve Patient
  // ==========================================================

  const resolvePatient = async (patientId) => {
    if (!threadId) return;

    setLoading(true);

    try {
      const response = await aiService.resolvePatient({
        thread_id: threadId,
        selected_patient_id: patientId,
      });

      console.log("RESOLVE PATIENT RESPONSE:", response);

      if (response?.interrupt) {
        const interruptData = response.interrupt;

        setInterrupt(interruptData);

        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            role: "assistant",
            title: interruptData.type || "Action Required",
            content: interruptData.message || "More information is required.",
            data: {
              patient: interruptData.patient || null,
              medications: interruptData.medications || [],
              recommendations: interruptData.ai_review?.recommendations || [],
              summary: interruptData.ai_review?.summary || "",
              requires_doctor_approval:
                interruptData.ai_review?.requires_doctor_approval || false,
            },
          },
        ]);

        return;
      }

      setInterrupt(null);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          response: response?.response,
          title: response?.response?.title || "Patient Selected",
          content:
            response?.response?.message || "Patient selected successfully.",
          data: response?.response?.data || null,
        },
      ]);
    } catch (err) {
      console.error("Resolve patient error:", err);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          title: "Error",
          content: err?.response?.data?.detail || "Unable to resolve patient.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // Bed Selection
  // ==========================================================

  const selectBed = async (data) => {
    if (!threadId) return;

    setLoading(true);

    try {
      const response = await aiService.selectBed({
        thread_id: threadId,
        ...data,
      });

      setInterrupt(null);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          response: response.response,
          title: response.response?.title || "Bed Assigned",
          content: response.response?.message || "Bed assigned successfully.",
          data: response.response?.data || null,
        },
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // Appointment Confirmation
  // ==========================================================

  const onAppointmentConfirmation = async ({ confirmed }) => {
    if (!threadId) return;

    setLoading(true);

    try {
      const response = await aiService.confirmAppointment({
        thread_id: threadId,
        confirmed,
      });

      console.log("APPOINTMENT CONFIRMATION RESPONSE:", response);

      // Another interrupt came from backend
      if (response?.interrupt) {
        const interruptData = response.interrupt;

        setInterrupt(interruptData);

        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            role: "assistant",
            title: interruptData.type || "Action Required",
            content: interruptData.message || "More information is required.",
            data: interruptData,
          },
        ]);

        return response;
      }

      // Workflow completed
      setInterrupt(null);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          response: response?.response,
          title: response?.response?.title || "Appointment Booking",
          content:
            response?.response?.message ||
            "Appointment booking completed successfully.",
          data: response?.response?.data || null,
        },
      ]);

      return response;
    } catch (err) {
      console.error("Appointment confirmation error:", err);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          title: "Error",
          content:
            err?.response?.data?.detail ||
            "Unable to process appointment confirmation.",
        },
      ]);

      throw err;
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // Clear Interrupt
  // ==========================================================

  const clearInterrupt = () => {
    setInterrupt(null);
  };

  // ==========================================================
  // New Chat
  // ==========================================================

  const newChat = () => {
    setThreadId(null);
    setInterrupt(null);

    setMessages([
      {
        id: Date.now(),
        role: "assistant",
        title: "AI Hospital Assistant",
        content: "👋 Hello Doctor! How can I help you today?",
      },
    ]);
  };

  return {
    messages,
    loading,
    interrupt,
    threadId,
    sendMessage,
    selectBed,
    resolvePatient,
    onAppointmentConfirmation,
    newChat,
    clearInterrupt,
  };
}
