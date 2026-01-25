// Для сервера
// export const BASE_URL = "/api/v1";

// Для локальной разработки 
export const BASE_URL = "http://127.0.0.1:8000/api/v1";


export const USER_ENDPOINTS = {
    LOGIN: "/auth/login/",
    REGISTER: "/auth/register/",
    REFRESH: "/auth/refresh/",
    SOCIAL: (provider) => `${BASE_URL}/social/${provider}/`
};

export const FOLDER_ENDPOINTS = {
    LIST: "/folders/",
    CREATE: "/folders/",
    RETRIEVE: (public_id) => `/folders/${public_id}/`,
    PATCH: (public_id) => `/folders/${public_id}/`,
    DELETE: (public_id) => `/folders/${public_id}/`
};

export const COURSE_ENDPOINTS = {
    LIST: "/courses/",
    CREATE: "/courses/",
    MY: "/courses/my_courses/",
    RETRIEVE: (public_id) => `/courses/${public_id}/`,
    PATCH: (public_id) => `/courses/${public_id}/`,
    DELETE: (public_id) => `/courses/${public_id}/`,
    TOGGLE_SUBSCRIPTION: (public_id) => `/courses/${public_id}/subscribe_unsubscribe/`,
    TOGGLE_REACTION: (public_id) => `/courses/${public_id}/like_dislike/`
};

export const IMAGE_ENDPOINTS={
    CREATE: "/images/", 
};

export const SOUND_ENDPOINTS={
    CREATE: "/sounds/", 
};

export const MODULE_ENDPOINTS = {
    CREATE: "/flashcards/",
    RETRIEVE: (public_id) => `/flashcards/${public_id}/`,
    PATCH: (public_id) => `/flashcards/${public_id}/`,
    DELETE: (public_id) => `/flashcards/${public_id}/`,

};

export const CARD_ENDPOINTS ={
    CREATE: "/cards/",
    RETRIEVE: (public_id) => `/cards/${public_id}/`,
    PATCH: (public_id) => `/cards/${public_id}/`,
    DELETE: (public_id) => `/cards/${public_id}/`,
};

export const STUDY_ENDPOINTS={
    RETRIEVE: (public_id) => `/study/${public_id}/`,
    POST: (public_id) => `/study/${public_id}/`,
    DELETE: (public_id) => `/study/${public_id}/`,
}

export const HISTORY_ENDPOINTS={
    RETRIEVE_CARD: (public_id) => `/study/history/cards/${public_id}/`,
    RETRIEVE_SESSIONS: (public_id) => `/study/${public_id}/history/sessions/`,
}
