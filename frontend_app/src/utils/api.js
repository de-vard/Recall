export const BASE_URL = "http://localhost:8000/api/v1";

export const USER_ENDPOINTS = {
    LOGIN: `${BASE_URL}/auth/login/`,
    REGISTER: `${BASE_URL}/auth/register/`,
    REFRESH: `${BASE_URL}/auth/refresh/`,
};

export const FOLDER_ENDPOINTS = {
    LIST: `${BASE_URL}/folders/`,
    CREATE: `${BASE_URL}/folders/`,
    RETRIEVE: (public_id) => `${BASE_URL}/folders/${public_id}/`,
    PATCH: (public_id) => `${BASE_URL}/folders/${public_id}/`,
    DELETE: (public_id) => `${BASE_URL}/folders/${public_id}/`
};

export const COURSE_ENDPOINTS = {
    LIST: `${BASE_URL}/courses/`,
    CREATE: `${BASE_URL}/courses/`,
    MY: `${BASE_URL}/courses/my_courses/`,
    RETRIEVE: (public_id) => `${BASE_URL}/courses/${public_id}/`,
    PATCH: (public_id) => `${BASE_URL}/courses/${public_id}/`,
    DELETE: (public_id) => `${BASE_URL}/courses/${public_id}/`,
    TOGGLE_SUBSCRIPTION: (public_id) => `${BASE_URL}/courses/${public_id}/subscribe_unsubscribe/`,
    TOGGLE_REACTION: (public_id) => `${BASE_URL}/courses/${public_id}/like_dislike/`
};

export const IMAGE_ENDPOINTS={
    CREATE: `${BASE_URL}/images/`, 
};

export const SOUND_ENDPOINTS={
    CREATE: `${BASE_URL}/sounds/`, 
};

export const MODULE_ENDPOINTS = {
    CREATE: `${BASE_URL}/flashcards/`,
    RETRIEVE: (public_id) => `${BASE_URL}/flashcards/${public_id}/`,
    PATCH: (public_id) => `${BASE_URL}/flashcards/${public_id}/`,
    DELETE: (public_id) => `${BASE_URL}/flashcards/${public_id}/`,

};

export const CARD_ENDPOINTS ={
    CREATE: `${BASE_URL}/cards/`,
    RETRIEVE: (public_id) => `${BASE_URL}/cards/${public_id}/`,
    PATCH: (public_id) => `${BASE_URL}/cards/${public_id}/`,
    DELETE: (public_id) => `${BASE_URL}/cards/${public_id}/`,
};

export const STUDY_ENDPOINTS={
    RETRIEVE: (public_id) => `${BASE_URL}/study/${public_id}/`,
    POST: (public_id) => `${BASE_URL}/study/${public_id}/`,
    DELETE: (public_id) => `${BASE_URL}/study/${public_id}/`,
}

export const HISTORY_ENDPOINTS={
    RETRIEVE_CARD: (public_id) => `${BASE_URL}/study/history/cards/${public_id}/`,
    RETRIEVE_SESSIONS: (public_id) => `${BASE_URL}/study/${public_id}/history/sessions/`,
}