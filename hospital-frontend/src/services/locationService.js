import api from "../api/axios";
const locationService = {
  createLocation: async (locationData) => {
    const response = await api.post("/locations", locationData);
    return response.data;
  },
};

export default locationService;
