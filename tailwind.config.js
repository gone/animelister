module.exports = {
  mode: 'jit',
  purge: [
    './frontend/**/*.html',
    './frontend/**/*.js',
    './frontend/**/*.css',
    './animelister/templates/**/*.html',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
