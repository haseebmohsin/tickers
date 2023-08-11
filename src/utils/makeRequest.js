import axios from 'axios';
import history from '../navigation';

const baseUrl = process.env.REACT_APP_BACKEND_URL;

const makeRequest = async ({ method = 'GET', path, data }) => {
  const url = `${baseUrl}/${path}`;

  const headers = {};

  const options = {
    method,
    url,
    headers,
    data,
  };

  if (method === 'POST' && !data) {
    return Promise.reject({ status: 400, error: 'Data is missing' });
  }

  if (method === 'PUT' && !data) {
    return Promise.reject({ status: 400, error: 'Data is missing' });
  }

  if (method === 'DELETE' && data) {
    return Promise.reject({ status: 400, error: 'Data should not be sent for DELETE requests' });
  }

  try {
    const response = await axios(options);
    return response.data;
  } catch (error) {
    if (error.message === 'Network Error') {
      return Promise.reject({ status: 500, message: 'Network Error' });
    }

    const { status, data } = error?.response;

    if (status === 404 || status === 500) {
      history.push('/errorPage');
    }

    return Promise.reject({ status, message: data?.error?.message });
  }
};

export default makeRequest;
