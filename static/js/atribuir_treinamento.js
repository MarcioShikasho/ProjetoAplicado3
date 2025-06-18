document.addEventListener('DOMContentLoaded', function () {
    const tipoAtribuicao = document.querySelectorAll('input[name="tipo_atribuicao"]');
    const divColaboradores = document.getElementById('div_colaboradores');
    const divCargo = document.getElementById('div_cargo');

    function toggleAtribuicao() {
        const selectedValue = document.querySelector('input[name="tipo_atribuicao"]:checked').value;
        divColaboradores.style.display = selectedValue === 'individual' ? 'block' : 'none';
        divCargo.style.display = selectedValue === 'cargo' ? 'block' : 'none';
    }

    toggleAtribuicao();

    tipoAtribuicao.forEach(radio => {
        radio.addEventListener('change', toggleAtribuicao);
    });
});
