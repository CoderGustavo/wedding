// script.js
$(document).ready(function () {
    $("form").on("submit", function (event) {
        event.preventDefault();

        const form = $(this);
        const formData = form.serializeArray();
        const jsonData = convertFormDataToJson(formData);

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
    $.ajax({
        url: url,
        method: method,
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function () {
            console.log("Formulário enviado com sucesso!");
        },
        error: function (xhr, status, error) {
            console.error("Erro ao enviar o formulário:", status, error);
        }
    });
}
