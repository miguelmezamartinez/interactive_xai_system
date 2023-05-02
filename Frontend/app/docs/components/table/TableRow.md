# TableRow

Component for a single table row

## Props

| Name                  | Type     | Description                                                              |
| --------------------- | -------- | ------------------------------------------------------------------------ |
| `row-data` *required* | `Object` | Object with the attributes and values to be displayed in this table row. |

## Computed Properties

| Name                 | Type      | Description                                                                                                                      |
| -------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `filteredAttributes` | `unknown` | Filters the attributes to exclude the special attributes id, NN_recommendation and NN_confidence<br/>**Dependencies:** `rowData` |

