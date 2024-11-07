// script.js
$(document).ready(function () {
    $("form").on("submit", function (event) {
        event.preventDefault();

        const form = $(this);
        const formData = form.serializeArray();
        const jsonData = convertFormDataToJson(formData);

        // Adiciona a chave da API manualmente ao JSON
        jsonData.apikey = "8201c3d9-60f7-41f5-a91b-a0ca0afaa0fc";

        sendForm(form.attr("action"), form.attr("method"), jsonData);
    });
});

function convertFormDataToJson(formData) {
    return formData.reduce((acc, field) => {
        acc[field.name] = field.value;
        return acc;
    }, {});
}

function sendForm(url, method, data) {
    fetch(url, {
        method: method, // Método (GET, POST, etc.)
        headers: {
            'Content-Type': 'application/json', // Define o tipo de conteúdo como JSON
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro na requisição: ' + response.status);
        }
        return response.json(); // Retorna a resposta como JSON, se necessário
    })
    .then(data => {
        console.log("Formulário enviado com sucesso!");
    })
    .catch(error => {
        console.error("Erro ao enviar o formulário:", error);
    });
}



