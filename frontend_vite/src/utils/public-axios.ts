import axios from 'axios';
import { baseUrl } from './helper';

const publicAxios = axios.create({
  // baseURL: `${baseUrl}/api`,
  baseURL: `${baseUrl}`,
});

export default publicAxios;
