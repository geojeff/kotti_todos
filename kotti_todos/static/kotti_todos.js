if(jQuery) (function(jQuery) {
    jQuery(document).ready(function() {
        jQuery.ias({
            container : '.todoitems',
            item: '.todoitem',
            pagination: '.pagination',
            next: '.next a',
            loader: '<img src="/static-kotti_todos/loader.gif" />',
            onRenderComplete: function(items) {
                if (jQuery.isFunction(jQuery.fn.ias_on_render_complete)) {
                    jQuery.fn.ias_on_render_complete();
                }
            }
        });
    });
})(jQuery);
