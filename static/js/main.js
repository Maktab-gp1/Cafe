(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 24,
        dots: true,
        loop: true,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
    
})(jQuery);

// counter 
$(document).ready(function(){
    $('.count').prop('disabled', true);
       $(document).on('click','.plus',function(){
        $('.count').val(parseInt($('.count').val()) + 1 );
    });
    $(document).on('click','.minus',function(){
        $('.count').val(parseInt($('.count').val()) - 1 );
            if ($('.count').val() == 0) {
                $('.count').val(1);
            }
        });
 });





// $('.btn-number').click(function(e) {
//     e.preventDefault();
  
//     fieldName = $(this).attr('data-field');
//     type = $(this).attr('data-type');
//     var input = $("input[name='" + fieldName + "']");
//     var currentVal = parseInt(input.val());
//     if (!isNaN(currentVal)) {
//       if (type == 'minus') {
  
//         if (currentVal > input.attr('min')) {
//           input.val(currentVal - 1).change();
//         }
//         if (parseInt(input.val()) == input.attr('min')) {
//           $(this).attr('disabled', true);
//         }
  
//       } else if (type == 'plus') {
  
//         if (currentVal < input.attr('max')) {
//           input.val(currentVal + 1).change();
//         }
//         if (parseInt(input.val()) == input.attr('max')) {
//           $(this).attr('disabled', true);
//         }
  
//       }
//     } else {
//       input.val(0);
//     }
//   });
//   $('.input-number').focusin(function() {
//     $(this).data('oldValue', $(this).val());
//   });
//   $('.input-number').change(function() {
  
//     minValue = parseInt($(this).attr('min'));
//     maxValue = parseInt($(this).attr('max'));
//     valueCurrent = parseInt($(this).val());
  
//     name = $(this).attr('name');
//     if (valueCurrent >= minValue) {
//       $(".btn-number[data-type='minus'][data-field='" + name + "']").removeAttr('disabled')
//     } else {
//       alert('Sorry, the minimum value was reached');
//       $(this).val($(this).data('oldValue'));
//     }
//     if (valueCurrent <= maxValue) {
//       $(".btn-number[data-type='plus'][data-field='" + name + "']").removeAttr('disabled')
//     } else {
//       alert('Sorry, the maximum value was reached');
//       $(this).val($(this).data('oldValue'));
//     }
  
//   });




// $(document).ready(function() {
//     $('.minus').click(function () {
//         var $input = $(this).parent().find('input');
//         var count = parseInt($input.val()) - 1;
//         count = count < 1 ? 0 : count;
//         $input.val(count);
//         $input.change();
//         return false;
//     });
//     $('.plus').click(function () {
//         var $input = $(this).parent().find('input');
//         $input.val(parseInt($input.val()) + 1);
//         $input.change();
//         return false;
//     });
// });