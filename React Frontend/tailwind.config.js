/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Updated Primary Color Palette to Aramex Red (#CC0000)
        primary: {
          50: '#fff1f1',   // Lightest shade
          100: '#ffe0e0',
          200: '#ffc7c7',
          300: '#ff9e9e',
          400: '#ff6b6b',
          500: '#ff3838',  // Mid tone
          600: '#cc0000',  // Main Aramex Red (#CC0000)
          700: '#a30000',
          800: '#7a0000',
          900: '#520000',  // Darkest shade
          950: '#2b0000',
        },
        // Kept the secondary color, you can update this if needed
        secondary: {
          500: '#f59e0b',
          600: '#d97706',
        }
      }
    },
  },
  plugins: [],
}