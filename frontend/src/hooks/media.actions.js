import axiosService from "../utils/axios";
import { IMAGE_ENDPOINTS, SOUND_ENDPOINTS } from "../utils/api.js";

export function useMedia() {
  const uploadImage = async (file) => {
    const fd = new FormData();
    fd.append("path_file", file);

    const { data } = await axiosService.post(IMAGE_ENDPOINTS.CREATE, fd, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    return data; 
  };

  const uploadSound = async (file) => {
    const fd = new FormData();
    fd.append("path_file", file);

    const { data } = await axiosService.post(SOUND_ENDPOINTS.CREATE, fd, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    return data;
  };

  return { uploadImage, uploadSound };
}