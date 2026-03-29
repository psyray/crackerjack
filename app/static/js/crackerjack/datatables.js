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

    /**
     * Individual column text search (see https://datatables.net/examples/api/multi_filter.html).
     * Requires a matching <tfoot> row aligned with columns; non-searchable columns are skipped.
     *
     * @param {DataTable.Api} api
     */
    function isDataTablesColumnSearchable(column) {
        if (typeof column.searchable === 'function') {
            return column.searchable();
        }
        var settings = column.settings()[0];
        var idx = column.index();
        var meta = settings.aoColumns && settings.aoColumns[idx];
        if (meta && Object.prototype.hasOwnProperty.call(meta, 'bSearchable')) {
            return meta.bSearchable !== false;
        }
        return true;
    }

    function attachIndividualColumnSearch(api) {
        api.columns().every(function () {
            var column = this;
            if (!isDataTablesColumnSearchable(column)) {
                return;
            }
            var $footer = $(column.footer());
            if (!$footer.length) {
                return;
            }
            var title = ($(column.header()).text() || '').trim();
            var placeholder = title ? 'Search ' + title : '';
            $('<input type="text" class="form-control form-control-sm" />')
                .attr('placeholder', placeholder)
                .appendTo($footer.empty())
                .on('keyup change clear', function () {
                    var val = this.value;
                    if (column.search() !== val) {
                        column.search(val).draw();
                    }
                });
        });
    }

    window.CJ_DataTables = {
        defaultOptions: function () {
            return deepMerge(defaults);
        },

        /**
         * @param {string|JQuery} selector
         * @param {object} [overrides] Shallow/deep merged into defaults (jQuery.extend deep).
         * @param {boolean} [overrides.individualColumnSearch] When true, wire per-column inputs in <tfoot>.
         * @returns {DataTable.Api|null}
         */
        init: function (selector, overrides) {
            var $table = $(selector);
            if (!$table.length) {
                return null;
            }
            overrides = overrides || {};
            var wantColumnSearch = !!overrides.individualColumnSearch;
            var userInitComplete = overrides.initComplete;
            var sanitized = $.extend(true, {}, overrides);
            delete sanitized.individualColumnSearch;
            var opts = deepMerge(defaults, sanitized);
            if (wantColumnSearch) {
                opts.initComplete = function () {
                    if (typeof userInitComplete === 'function') {
                        userInitComplete.apply(this, arguments);
                    }
                    attachIndividualColumnSearch(this.api());
                };
            }
            return $table.DataTable(opts);
        }
    };
})(window, jQuery);
