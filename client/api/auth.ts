import api from './axios';

const authApi = '/api/auth';
export const login = async (email: string, password: string) => {
  try {
    const response = await api.post(`${authApi}/login`, { email, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const register = async (name: string, email: string, password: string) => {
  try {
    const response = await api.post(`${authApi}/register`, { name, email, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};
