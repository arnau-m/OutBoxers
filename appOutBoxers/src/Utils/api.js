import axios from 'axios';

// Configuración de Axios
const apiClient = axios.create({
  baseURL: 'https://ra-develop.iotlab.connect.bobst.com/external/api/',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Interceptor de solicitud para agregar apiKey
apiClient.interceptors.request.use(
  (config) => {
    // Agrega apiKey a los parámetros de consulta
    config.params = {
      ...config.params,
      apiKey: '230f3d62bcf74b419911dca4da40944d',
    };
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor de respuesta
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error('Error de respuesta:', error.response.data);
    } else if (error.request) {
      console.error('Error de solicitud:', error.request);
    } else {
      console.error('Error de configuración:', error.message);
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

// Métodos para interactuar con la API
const api = {
  get: async (url, queryParams) => {
    try {
      const response = await apiClient.get(url, { params: queryParams });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  post: async (url, data, queryParams) => {
    try {
      const response = await apiClient.post(url, data, { params: queryParams });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  put: async (url, data, queryParams) => {
    try {
      const response = await apiClient.put(url, data, { params: queryParams });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  delete: async (url, queryParams) => {
    try {
      const response = await apiClient.delete(url, { params: queryParams });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default api;
