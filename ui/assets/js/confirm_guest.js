$(async () => {
    // Funções para controlar o modal
    const modal = $("#modal");

    const btn_open_modal = $("#open_modal_confirm_guest");
    const btn_close_modal = $(".close_modal_confirm_guest");

    const field_phone = $("[name='phone']");

    const get_cookie = (cookie_name) => {
        const cookies = document.cookie.split(';');
        for(let cookie of cookies) {
            const [nome, valor] = cookie.split('=');
            if(nome.trim() === cookie_name) {
                return decodeURIComponent(valor);
            }
        }
        return '';
    }

    const format_phone = (value) => {
        value = value.replace(/\D/g, ''); // Remove tudo que não for número

        if (value.length > 11) {
            value = value.slice(0, 11); // Limita a 11 dígitos
        }

        let formattedValue = '';

        if (value.length > 0) {
            formattedValue = `(${value.slice(0, 2)}) `; // Código de área

            if (value.length > 2) {
                formattedValue += `${value.slice(2, 7)}`; // Primeira parte do número

                if (value.length > 7) {
                    formattedValue += `-${value.slice(7, 11)}`; // Segunda parte do número
                }
            }
        }
        return formattedValue;
    }

    field_phone.on('input', function(e) {
        e.target.value = format_phone(e.target.value);
    });

    field_phone.val(format_phone(get_cookie("phone")));

    const btn_confirm_guest = $("#btn_confirm_guest");

    const name_confirmed_content = $("#names_confirmed");
    const name_to_confirm_content = $("#names_to_confirm");

    const openModal = () => {
        modal.removeClass("hidden");
        modal.addClass("flex");
        setTimeout(() => {
            modal.css({
                "background-color": "rgba(0, 0, 0, 0.5)",
            });
            $("#modal > div").css({
                "margin-bottom": 0,
            });
        }, 50);
    };

    const closeModal = () => {
        modal.css({
            "background-color": "transparent",
        });
        $("#modal > div").css({
            "margin-bottom": "-100%",
        });
        setTimeout(() => {
            modal.addClass("hidden");
            modal.removeClass("flex");
        }, 500);
    };

    const error_message = (message = "") => {
        if (message) {
            $("#has_error").removeClass("hidden");
            $("#has_error").addClass("flex");
            $("#has_error").text(message);
        } else {
            $("#has_error").addClass("hidden");
            $("#has_error").removeClass("flex");
            $("#has_error").text("Sem erros.");
        }
    };

    const getGuests = async (phone) => {
        try {
            const guestsResponse = await fetch(
                `http://localhost:8000/api/guests/phone/${phone.toString()}`
            );

            if (!guestsResponse.ok) {
                throw new Error("Erro na requisição dos nomes");
            }

            guests = await guestsResponse.json();

            return guests.guests;
        } catch (error) {
            console.error("Erro ao carregar nomes:", error);
        }
    };

    const template_names = (item) => {
        if (item.confirmed) {
            return `
                <ul class="list-disc pl-5">
                    <li>
                        <span class="text-gray-300 peer-checked:text-lime-700 transition-colors duration-200">${item.name} | ${item.role}</span>
                    </li>
                </ul>
        `;
        }
        else {
            return `
                <label class="guests_data flex items-center space-x-3 cursor-pointer group shadow-lg bg-gray-800 border border-gray-800 hover:border-lime-800 rounded w-full py-4 px-2">
                    <input type="checkbox" class="opacity-0 absolute h-0 w-0 peer" name="guests" value="${item.id}">
                    <div class="w-6 h-6 border border-gray-300 rounded-lg flex items-center justify-center
                                peer-checked:bg-lime-800 peer-checked:border-lime-800
                                group-hover:border-lime-800">
                        <svg class="w-4 h-4 text-gray-800 peer-checked:text-white transition-opacity duration-200" viewBox="0 0 24 24">
                            <path d="M20 6L9 17l-5-5" stroke="currentColor" fill="none" stroke-width="2"
                                    stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <span class="text-gray-300 peer-checked:text-lime-700 transition-colors duration-200">${item.name} | ${item.role}</span>
                </label>
            `;
        }
    };

    const populate_names = async () => {
        phone = field_phone.val();
        name_confirmed_content.empty();
        name_to_confirm_content.empty();
        guests = await getGuests(phone);

        count_guests = 0;
        count_guests_confirmed = 0;


        guests.forEach((guest) => {
            guest.confirmed_txt = "Ainda não confirmado";
            if (guest.confirmed) {
                guest.confirmed_txt = "Já confirmado";
                count_guests_confirmed += 1;
                name_confirmed_content.append(template_names(guest));
            }else{
                name_to_confirm_content.append(template_names(guest));
            }
            count_guests += 1;
        });

        return {count_guests, count_guests_confirmed};
    };

    const toggle_element = (css_class, action) => {
        if (action == "show") {
            $(css_class).removeClass("hidden");
            $(css_class).addClass("flex");
        } else {
            $(css_class).addClass("hidden");
            $(css_class).removeClass("flex");
        }
    }

    btn_open_modal.on("click", async () => {
        if (!field_phone.val()) {
            error_message("O campo de telefone deve ser preenchido.");
            return;
        }
        error_message();
        $(".guests_data").remove();
        toggle_element(".loading_guests", "show");
        toggle_element(".footer-modal-confirm-guest", "show");
        toggle_element(".message-modal-confirmed-guest", "hide");
        toggle_element(".message-modal-to-confirm-guest", "hide");
        toggle_element("#names_to_confirm", "hide");
        toggle_element("#names_confirmed", "hide");
        $(".subtitle-modal").text("Selecione o nome da pessoa para confirmar a presença")
        openModal();
        const {count_guests, count_guests_confirmed} = await populate_names();
        toggle_element(".loading_guests", "hide");
        if (count_guests > 0) {
            toggle_element("#names_to_confirm", "show");
            toggle_element(".message-modal-to-confirm-guest", "show");
            $(".message-modal-to-confirm-guest").text("Convidados ainda não confirmados:");
        }
        if (count_guests_confirmed > 0) {
            if ( count_guests_confirmed === count_guests) {
                toggle_element(".footer-modal-confirm-guest", "hide");
                toggle_element(".message-modal-to-confirm-guest", "hide");
            }
            toggle_element("#names_confirmed", "show");
            toggle_element(".message-modal-confirmed-guest", "show");
            $(".subtitle-modal").text("Ficaremos muito felizes em ver vocês em nossa cerimônia!")
            $(".message-modal-confirmed-guest").text("Todos os convidados abaixo já confirmaram a presença:");
        }
        if (count_guests == 0 && count_guests_confirmed == 0) {
            toggle_element(".message-modal-confirmed-guest", "show");
            $(".subtitle-modal").text("Nenhum convidado encontrado");
            $(".message-modal-confirmed-guest").text("Nenhum convidado encontrado para esse número, insira o seu número de telefone corretamente.");
        }
    });

    btn_close_modal.on("click", () => {
        closeModal();
    });

    modal.on("click", (e) => {
        if (e.target === modal[0]) {
            closeModal();
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !modal.hasClass("hidden")) {
            closeModal();
        }
    });

    const confirm_guest = async (guest_id) => {
        const data = new URLSearchParams();
        data.append("guest_id", guest_id);
        data.append("confirmed", true);

        confirmationResponse = await fetch(
            `http://localhost:8000/api/confirmations/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: data.toString(),
            }
        );
        if (!confirmationResponse.ok) {
            throw new Error("Erro ao criar confirmação");
        }

        confirmation = await confirmationResponse.json();
        return confirmation;
    };

    btn_confirm_guest.on("click", () => {
        guests = $("[name='guests']:checked");
        guests.each((index) => {
            guest_id = $($(guests)[index]).val();
            guest = confirm_guest(guest_id)
        });
        closeModal();
        toggle_element("#modal_success", "show");
        setTimeout(() => {
            $("#modal_success > div").removeClass("scale-0");
            $("#modal_success > div").addClass("scale-1");
        }, 500);
    });
});
