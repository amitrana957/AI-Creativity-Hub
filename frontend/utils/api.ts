import axiosClient from "./axiosClient";

// ---------- TEXT CHAT ----------
export const askText = async (query: string, sessionId: string) => {
  try {
    const res = await axiosClient.post("/text/ask", {
      query,
      session_id: sessionId,
    });
    return res.data;
  } catch (error: any) {
    console.error("askText Error:", error.response?.data || error.message);
    throw error;
  }
};

// ---------- IMAGE GENERATION ----------
export const generateImage = async (prompt: string) => {
  try {
    const res = await axiosClient.post("/image/generate", { prompt });
    return res.data;
  } catch (error: any) {
    console.error("generateImage Error:", error.response?.data || error.message);
    throw error;
  }
};

// ---------- TTS (Text → Speech) ----------
export const generateStory = async (topic: string, session_id: string) => {
  try {
    const res = await axiosClient.post("/audio/generate-story", { topic, session_id });
    return res.data;
  } catch (error: any) {
    console.error("generateStory Error:", error.response?.data || error.message);
    throw error;
  }
};

// ---------- STT (Speech → Text) ----------
// api.ts
export const transcribeAudio = async (file: File | Blob, session_id: string) => {
  try {
    const formData = new FormData();

    // If file is a Blob but not File, convert to File
    const fileForUpload = file instanceof File ? file : new File([file], "audio.mp3", { type: "audio/mpeg" });

    formData.append("file", fileForUpload);
    formData.append("session_id", session_id);

    const res = await axiosClient.post("/audio/transcribe", formData, {
      // Axios automatically sets Content-Type to multipart/form-data with boundary
    });

    return res.data; // { transcript }
  } catch (error: any) {
    console.error("transcribeAudio Error:", error.response?.data || error.message);
    throw error;
  }
};

// ---------- MULTIMODAL ----------
export const multimodalTask = async (payload: any) => {
  try {
    const res = await axiosClient.post("/multimodal/process", payload);
    return res.data;
  } catch (error: any) {
    console.error("multimodalTask Error:", error.response?.data || error.message);
    throw error;
  }
};
