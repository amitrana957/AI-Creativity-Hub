import axiosClient from "./axiosClient";

export const askText = async (query: string) => {
  try {
    const res = await axiosClient.post("/text/ask", { query });
    return res.data;
  } catch (error: any) {
    console.error("askText Error:", error.response?.data || error.message);
    throw error;
  }
};

export const generateImage = async (prompt: string) => {
  try {
    const res = await axiosClient.post("/image/generate", { prompt });
    return res.data;
  } catch (error: any) {
    console.error("generateImage Error:", error.response?.data || error.message);
    throw error;
  }
};

export const transcribeAudio = async (file: any) => {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axiosClient.post("/audio/transcribe", formData, { headers: { "Content-Type": "multipart/form-data" } });
    return res.data;
  } catch (error: any) {
    console.error("transcribeAudio Error:", error.response?.data || error.message);
    throw error;
  }
};

export const multimodalTask = async (payload: any) => {
  try {
    const res = await axiosClient.post("/multimodal/process", payload);
    return res.data;
  } catch (error: any) {
    console.error("multimodalTask Error:", error.response?.data || error.message);
    throw error;
  }
};
