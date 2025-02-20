/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html", "*.html"],
  theme: {
    extend: {
      colors: {
        olive: {
          "100": "#A6C68D", // Verde oliva claro com maior saturação
          "200": "#7B9E57", // Verde oliva padrão mais vivo
          "300": "#597439", // Verde oliva escuro mais intenso
        },
        serenity: {
          "100": "#CBEAFF", // Azul serenity claro com boa saturação
          "200": "#B6DBF8", // Azul serenity claro com boa saturação
          "300": "#98C4EB", // Azul serenity padrão mais suave e equilibrado
          "400": "#73ADDB", // Azul serenity escuro, mas ainda vibrante e legível
        },
        lavanda: {
          "100": "#F3E9FF", // Lavanda claro mais vibrante
          "200": "#D9BFFF", // Lavanda padrão mais saturado
          "300": "#B892E3", // Lavanda escuro mais intenso
        },
      },
    },
  },
  plugins: [],
}

