// script.js
$(document).ready(function () {
    $("form").on("submit", function (event) {
        event.preventDefault();

        const form = $(this);
        const formType = form.attr("enctype") || "application/x-www-form-urlencoded";
        const formData = form.serializeArray();
        let data;

        if (formType === "application/json") {
            data = convertFormDataToJson(formData);
            data.apikey = "8201c3d9-60f7-41f5-a91b-a0ca0afaa0fc";
        } else {
            data = new URLSearchParams(formData.map(x => [x.name, x.value]));
            data.append("apikey", "8201c3d9-60f7-41f5-a91b-a0ca0afaa0fc");
        }

        sendForm(form.attr("action"), form.attr("method"), data, formType);
    });
});

function convertFormDataToJson(formData) {
    return formData.reduce((acc, field) => {
        acc[field.name] = field.value;
        return acc;
    }, {});
}

function sendForm(url, method, data, contentType) {
    const headers = {
        'Content-Type': contentType
    };
    
    const body = contentType === "application/json" ? 
        JSON.stringify(data) : 
        data.toString();

    fetch(url, {
        method: method,
        headers: headers,
        body: body
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro na requisição: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log("Formulário enviado com sucesso!");
    })
    .catch(error => {
        console.error("Erro ao enviar o formulário:", error);
    });
}
