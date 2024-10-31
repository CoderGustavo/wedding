$(document).ready(function() {
    $("a").on("click", (e) => {
        e.preventDefault();
        url = e.currentTarget.href
        content = $("#content")
            $.get(url, (data) => {
                content.css("opacity", 0)
                setTimeout(() => {
                    content.html(data)
                    content.css("opacity", 1)
                    history.pushState(null, null, url)
                }, 500);
            }).fail(() => {
                alert("Erro ao carregar a pagina")
            })
    })

    window.onpopstate = function() {
        const url = location.pathname.substring(1);
        $.get(url, function(data) {
            $('#conteudo').html(data).fadeIn(300);
        }).fail(function() {
            console.error('Erro ao carregar a página');
        });
    };
});
