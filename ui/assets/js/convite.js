$(document).ready(function () {

    const element_name = $("#name")

    const queryString = window.location.search;

    const urlParams = new URLSearchParams(queryString);

    const nome = urlParams.get("nome") || "desconhecido"
    const phone = urlParams.get("phone") || ""

    document.cookie = `nome=${nome}; max-age=${60*60*24*30}; path=/`;
    document.cookie = `phone=${phone}; max-age=${60*60*24*30}; path=/`;

    element_name.text(nome)
});
