import colors from 'tailwindcss/colors';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        // The brand color. Components use primary-*, so changing it here restyles the app;
        // red-* stays reserved for error states.
        primary: colors.red,
      },
    },
  },
  plugins: [],
};
