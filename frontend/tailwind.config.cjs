/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}",],
  theme: {
    extend: {},
    colors: {
      transparent: 'transparent',
      'white': '#ffffff',
      'black': '#000000',
      'light-silver': '#d8d8d8',
      'davy-gray': '#585858',
      'alabaster': '#e9e9ed',
      'chinese-silver': '#cacaca',
      'pastel-gray': '#d6ccc2',
      'bone': '#E3D5CA',
      'bermuda': '#78dcca',
    },
  },
  plugins: [],
}
