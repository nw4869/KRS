$(function () {
    $(".confirm-alert").on('click', function (e) {
        if (!confirm('确认要执行这个操作？')) {
            return e.preventDefault();
        }
    });
});
