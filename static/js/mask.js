console.log("mask.js atualizado!");

// Aplicar em inputs com nomes relacionados a data, mesmo sem .datamask
var dateInputs = $("input[name*='data'], input[id*='data'], input[placeholder*='dd/mm'], input[type='date'], .datamask");

dateInputs.each(function () {
    if ($(this).attr('type') === 'date') {
        $(this).attr('type', 'text');
    }

    $(this).inputmask({
        mask: "99/99/9999",
        placeholder: "dd/mm/aaaa",
        showMaskOnHover: true,
        showMaskOnFocus: true,
        insertMode: false,
        clearMaskOnLostFocus: false
    });

    $(this).on("keydown", function (e) {
        if ((e.key >= '0' && e.key <= '9') || e.keyCode === 8) {
            let curPos = this.selectionStart;
            if ((curPos === 2 || curPos === 5) && e.keyCode !== 8) {
                e.preventDefault();
                setTimeout(() => {
                    this.setSelectionRange(curPos + 1, curPos + 1);
                    let newEvent = new KeyboardEvent('keydown', e);
                    this.dispatchEvent(newEvent);
                }, 5);
            }
        }
    });

    $(this).on("focus", function () {
        $(this).select();
    });
});

// Máscara para CPF
$(".cpfmask").inputmask({
    mask: ["999.999.999-99"],
    showMaskOnHover: true,
    showMaskOnFocus: true
});

// Máscara para telefone
$(".phonemask").inputmask({
    mask: ["(99) 9999-9999", "(99) 99999-9999"],
    keepStatic: true,
    showMaskOnHover: true,
    showMaskOnFocus: true
});

// Selecionar tudo ao focar (CPF/Telefone)
$(".cpfmask, .phonemask").on("focus", function () {
    $(this).select();
});
