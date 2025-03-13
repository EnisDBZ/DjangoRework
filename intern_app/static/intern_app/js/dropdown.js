// Show dropdown on hover
$('.dropdown').mouseover(function () {
    if($('.navbar-toggler').is(':hidden')) {
        $(this).addClass('show').attr('aria-expanded', 'true');
        $(this).find('.dropdown-menu').addClass('show');
    }
}).mouseout(function () {
    if($('.navbar-toggler').is(':hidden')) {
        $(this).removeClass('show').attr('aria-expanded', 'false');
        $(this).find('.dropdown-menu').removeClass('show');
    }
});

// Go to the parent link on click
$('.dropdown > a').click(function(){
    location.href = this.href;
});
