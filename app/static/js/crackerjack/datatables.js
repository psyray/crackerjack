/**
 * Shared DataTables defaults for CrackerJack (Bootstrap 4 + Responsive).
 * Load after jQuery and static/js/lib/datatables.min.js (bundle must include Responsive).
 */
(function (window, $) {
    'use strict';

    var defaults = {
        responsive: true,
        autoWidth: false,
        language: {
            search: 'Filter:',
            lengthMenu: 'Show _MENU_ entries'
        },
        pageLength: 25
    };

    function deepMerge(target, source) {
        return $.extend(true, {}, target, source || {});
    }

    window.CJ_DataTables = {
        defaultOptions: function () {
            return deepMerge(defaults);
        },

        /**
         * @param {string|JQuery} selector
         * @param {object} [overrides] Shallow/deep merged into defaults (jQuery.extend deep).
         * @returns {DataTable.Api|null}
         */
        init: function (selector, overrides) {
            var $table = $(selector);
            if (!$table.length) {
                return null;
            }
            return $table.DataTable(deepMerge(defaults, overrides));
        }
    };
})(window, jQuery);
