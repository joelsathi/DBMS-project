const CURRENCRY_FORMATTER = new Intl.NumberFormat(undefined, {
  currency: 'USD',
  style: 'currency',
});

export const formatCurrencry = (number: any) => {
  return CURRENCRY_FORMATTER.format(number);
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

export const baseUrl =
  import.meta.env.VITE_MODE === 'development'
    ? 'http://127.0.0.1:8000'
    : 'http://127.0.0.1:8000';