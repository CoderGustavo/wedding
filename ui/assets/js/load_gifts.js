$(async () => {
    // Get elements to append dynamic alements
    let $categoriesList = $(".categories-list");
    let $sectionsList = $("#all-content");

    // Initialize data list
    let categoriesData = null;
    let giftsData = null;

    async function loadData() {
        try {
            // Executa as duas requisições em paralelo
            const [categoriesResponse, giftsResponse] = await Promise.all([
                fetch("http://localhost:8000/api/categories"),
                fetch("http://localhost:8000/api/gifts"),
            ]);

            // Verifica se as respostas foram bem-sucedidas
            if (!categoriesResponse.ok) {
                throw new Error("Erro na requisição de categorias");
            }
            if (!giftsResponse.ok) {
                throw new Error("Erro na requisição de presentes");
            }

            // Atribui os dados às variáveis globais
            categoriesData = await categoriesResponse.json();
            giftsData = await giftsResponse.json();
        } catch (error) {
            console.error("Erro ao carregar dados:", error);
        }
    }

    template_categories = (item) => `
        <a
            href="${item.name_with_underline}"
            class="max-w-[250px] flex-shrink-0 flex flex-col items-center"
        >
            <img
                class="w-32 h-32 md:w-40 md:h-40 object-cover rounded-full shadow-lg"
                src="${item.picture}"
                alt="Foto ${item.name}"
            >
            <div class="p-4">
                <h2
                    class="text-md md:text-lg font-semibold"
                >
                    ${item.name}
                </h2>
            </div>
        </a>
    `;

    template_gift = (item) => `
        <a
        href="${item.payment_url}"
        class="p-0 m-0"
        >
            <div
            class="max-w-[200px] md:max-w-[300px] mx-auto overflow-hidden hover:bg-gray-200 transition-colors p-2 rounded"
            >
                <img
                    src="${item.image}"
                    class="w-full h-72 object-cover shadow-lg relative rounded"
                >
                <div class="p-4">
                    <h3
                        class="text-lg font-semibold text-gray-900 rounded-full"
                    >
                        ${item.name}
                    </h3>
                    <span
                        class="text-md font-bold text-gray-700 rounded-full"
                    >R$ ${item.price}</span>
                    <a
                        href="${item.payment_url}"
                        class="block px-4 py-2 bg-lime-800 w-full text-white text-sm font-semibold rounded hover:bg-lime-500 mt-4"
                    >
                        Escolher esse presente
                    </a>
                </div>
            </div>
        </a>
    `;

    template_section = (item) => `
        <section id="${item.name_with_underline}" class="flex flex-col gap-8">
            <h2
                class="text-lg md:text-2xl font-bold font-serif uppercase size-fit mx-auto rounded-full"
            >
                ${item.name}
            </h2>
            <div class="flex flex-wrap gap-2 md:gap4">
                ${item.gifts}
            </div>
        </section>
    `;

    populate_categories = (categories_data) => {
        categories_data.forEach((item) => {
            item.name_with_underline = item.name
                .toLowerCase()
                .replace(/ /g, "_");
            $categoriesList.append(template_categories(item));
        });
    };

    populate_sections = (categories_data) => {
        categories_data.forEach((category_item) => {
            category_item.name_with_underline = category_item.name
                .toLowerCase()
                .replace(/ /g, "_");
            const gifts_data = giftsData.gifts;
            let gift_elements = "";
            gifts_data.forEach((gift_item) => {
                if (category_item.name == gift_item.category) {
                    gift_elements += template_gift(gift_item);
                }
            });
            category_item.gifts = gift_elements;
            $sectionsList.append(template_section(category_item));
        });
    };

    await loadData();

    $(".remove-on-load").remove();
    populate_categories(categoriesData.categories);
    populate_sections(categoriesData.categories);
});
