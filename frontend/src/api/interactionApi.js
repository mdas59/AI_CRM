import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const createInteraction = async (interactionData) => {
  const response = await axios.post(
    `${API_BASE_URL}/interactions/`,
    interactionData
  );

  return response.data;
};

export const getInteractions = async () => {
  const response = await axios.get(
    `${API_BASE_URL}/interactions/`
  );
  return response.data;
};


export const runAgent = async (message) => {
  const response = await axios.post(
    `${API_BASE_URL}/ai/agent`,
    { message }
  );
  return response.data;
};