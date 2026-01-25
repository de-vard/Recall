import axios from "axios";
import createAuthRefreshInterceptor from "axios-auth-refresh";
import { BASE_URL, USER_ENDPOINTS } from "./api";
import { getAccessToken, getUser, getRefreshToken } from "../hooks/user.actions";

const axiosService = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosService.interceptors.request.use((config) => {
  const auth = JSON.parse(localStorage.getItem("auth") || "{}");
  if (auth?.access) {
    config.headers.Authorization = `Bearer ${auth.access}`;
  }
  return config;
});

axiosService.interceptors.response.use(
  (res) => res,
  (err) => Promise.reject(err),
);

// const refreshAuthLogic = async (failedRequest) => {
//     // когда включаю сервер и запускаю реакт приложение не идет ридерек на форму входа а возникают ошибки :8000/api/v1/folders/:1 Failed to load resource: the server responded with a status of 401 (Unauthorized) :8000/api/v1/folders/:1 Failed to load resource: the server responded with a status of 401 (Unauthorized) :8000/api/v1/auth/refresh/:1 Failed to load resource: the server responded with a status of 401 (Unauthorized)

//     const oldAuth = JSON.parse(localStorage.getItem("auth") || "{}");

//     if (!oldAuth?.refresh) {
//         window.location.href = "/login";
//         return Promise.reject();
//     }

//     try {
//         const { data } = await axiosService.post(USER_ENDPOINTS.REFRESH, { refresh: oldAuth.refresh });
//         const { access, refresh } = data;

//         failedRequest.response.config.headers["Authorization"] = `Bearer ${access}`;

//         localStorage.setItem("auth", JSON.stringify({ access, refresh, user: oldAuth.user }));
//         return Promise.resolve();
//     } catch (error) {
//         if ([400, 401].includes(error.response?.status)) {
//             localStorage.removeItem("auth");
//             window.location.href = "/login";
//         }
//         return Promise.reject(error);
//     }
// };

const refreshAuthLogic = async (failedRequest) => {
  return axios

    .post(
      `${BASE_URL}${USER_ENDPOINTS.REFRESH}`,
      { refresh: getRefreshToken() },
      { baseURL: BASE_URL },
    )
    .then((resp) => {
      const { access } = resp.data;
      failedRequest.response.config.headers["Authorization"] =
        "Bearer " + access;
      localStorage.setItem(
        "auth",
        JSON.stringify({
          access,
          refresh: getRefreshToken(),
          user: getUser(),
        }),
      );
    })
    .catch(() => {
      localStorage.removeItem("auth");
    });
};

createAuthRefreshInterceptor(axiosService, refreshAuthLogic);

export const fetcher = (url) => axiosService.get(url).then((res) => res.data);

export default axiosService;
