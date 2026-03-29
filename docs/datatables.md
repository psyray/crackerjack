# DataTables and Responsive layout

CrackerJack ships a single minified bundle for tables:

* `app/static/js/lib/datatables.min.js`
* `app/static/css/lib/datatables.min.css`

The bundle is built from the [DataTables download builder](https://datatables.net/download) (Bootstrap 4 styling + core + **Responsive** extension). The header inside `datatables.min.js` records the exact combination (for example DataTables core and Responsive versions).

Do not load a second copy of DataTables or Responsive on the same page.

## Viewport

Responsive relies on a proper viewport meta tag (see `app/templates/layout/head.html`). See also the [Responsive extension manual](https://datatables.net/extensions/responsive/).

## Layout classes (DataTables 2.x)

The Bootstrap 4 combined bundle uses `div.dt-container` around the table, with `div.dt-length`, `div.dt-search`, `div.dt-info`, and `div.dt-paging` for controls. Older tutorials referencing `dataTables_wrapper` / `dataTables_filter` apply to DataTables 1.x only.

## Shared initialisation

Use `app/static/js/crackerjack/datatables.js`, which exposes `CJ_DataTables`:

* `CJ_DataTables.defaultOptions()` — copy of shared defaults (`responsive: true`, DataTables 2 default `layout`, no `scrollX` by default).
* `CJ_DataTables.init(selector, overrides)` — merges overrides into defaults and calls `.DataTable(...)`.

### Individual column searching

To enable per-column text filters (cumulative with the global search), set `individualColumnSearch: true` and add a `<tfoot>` row whose `<th>` cells align with `<thead>` (same column count and order, including conditional columns). See the [DataTables example](https://datatables.net/examples/api/multi_filter.html).

`CJ_DataTables` strips `individualColumnSearch` before passing options to DataTables and wires `column().search()` from inputs in the footer. Columns marked non-searchable (for example action buttons) get no input.

Load order on a page:

1. jQuery (already in `layout/head.html`)
2. `datatables.min.js`
3. `datatables.js`
4. Page-specific script

Example (Browse cracked passwords):

```javascript
CJ_DataTables.init('.table-cracked', { pageLength: 100, individualColumnSearch: true });
```

Example (Dashboard session list, `home/index.html`):

```javascript
CJ_DataTables.init('.table-sessions-list', {
    order: [[0, 'desc']],
    language: { search: 'Search sessions:' },
    columnDefs: [{ targets: -1, orderable: false, searchable: false }],
    individualColumnSearch: true
});
```

## Column visibility

For the Responsive extension, prefer:

* Header cell classes such as `all` (always visible in the main table) where appropriate; see [class logic](https://datatables.net/extensions/responsive/classes).
* Or `columnDefs` with `responsivePriority` (lower values are affected first when the table is narrowed).

Avoid enabling `scrollX` globally unless a specific table needs horizontal scroll in addition to Responsive.

## Manual checks

After UI changes, spot-check at roughly 390px, 768px, and desktop widths: collapsed columns, child-row details, filter/length/pagination controls, and desktop layout.
