document.addEventListener('DOMContentLoaded', function () {
    // Campos de exibição condicional
    const tipoAtribuicao = document.querySelectorAll('input[name="tipo_atribuicao"]');
    const divColaboradores = document.getElementById('div_colaboradores');
    const divCargo = document.getElementById('div_cargo');

    // Função para alternar visibilidade entre colaborador/cargo
    function toggleAtribuicao() {
        const selectedValue = document.querySelector('input[name="tipo_atribuicao"]:checked').value;

        if (selectedValue === 'individual') {
            divColaboradores.style.display = 'block';
            divCargo.style.display = 'none';
        } else if (selectedValue === 'cargo') {
            divColaboradores.style.display = 'none';
            divCargo.style.display = 'block';
        }
    }

    // Inicializa a exibição correta ao carregar a página
    toggleAtribuicao();

    // Atualiza visibilidade ao trocar o tipo
    tipoAtribuicao.forEach(radio => {
        radio.addEventListener('change', toggleAtribuicao);
    });

    // Inicializa o Select2 se disponível
    if (typeof $ !== 'undefined' && $.fn.select2) {
        $(document).ready(function () {
    setTimeout(() => {
        $('#id_colaboradores').select2({
            placeholder: 'Selecione os colaboradores',
            width: '100%',
            allowClear: true
        });
    }, 100);
    })}

    // AJAX para carregar colaboradores por cargo
    $('#id_cargo').change(function () {
        const cargoId = $(this).val();

        $.ajax({
            url: URL_CARREGAR_COLABORADORES,
            data: { cargo: cargoId },
            success: function (data) {
                let select = $('#id_colaboradores');
                select.empty();

                if (data.length === 0) {
                    select.append('<option value="">Nenhum colaborador encontrado</option>');
                } else {
                    data.forEach(function (colab) {
                        select.append(`<option value="${colab.id}">${colab.nome}</option>`);
                    });
                }

                select.select2({
                    placeholder: 'Selecione os colaboradores',
                    width: '100%',
                    allowClear: true
                });
            },
            error: function () {
                console.error('Erro ao carregar colaboradores via AJAX.');
            }
        });
    });
});
