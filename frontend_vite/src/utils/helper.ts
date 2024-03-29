const CURRENCY_FORMATTER = new Intl.NumberFormat(undefined, {
  currency: 'LKR',
  style: 'currency',
});

export const formatCurrency = (number: any) => {
  return CURRENCY_FORMATTER.format(number);
};

export const getDate = (date: Date) => {
  return new Date(date).toLocaleDateString('en');
};
// backend server url(replace with fastapi server url)
// export const baseUrl =
//   import.meta.env.VITE_MODE === 'development'
//     ? 'http://localhost:5000'
//     : 'https://typeshop-server.onrender.com';
// to check with a empty database
// export const baseUrl =
//   import.meta.env.VITE_MODE === 'development'
//     ? ''
//     : '';


// fastapi server url

// export const baseUrl =
//   import.meta.env.VITE_MODE === 'development'
//     ? 'http://127.0.0.1:8000'
//     : 'http://127.0.0.1:8000';
export const baseUrl =
import.meta.env.VITE_MODE === 'development'
  ? 'http://159.89.169.248/api'
  : 'http://159.89.169.248/api';