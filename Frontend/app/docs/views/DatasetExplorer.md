# DatasetExplorer

Component for the Dataset Explore page. Contains a navigation button, filter and
customize buttons and the Data Table.

## Data

| Name              | Type      | Description                                      | Initial value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----------------- | --------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `toggleCustomize` | `boolean` | Indicates if the customize overlay is shown      | `false`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `toggleFilter`    | `boolean` | Indicates if the filter overlay is shown         | `false`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `isAtPageTop`     | `boolean` | Indicates if user is at the top of page          | `true`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `tableRows`       | `array`   | The table rows to be displayed in the Data Table | `[]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `requestBody`     | `object`  | Request body for the POST /table request         | `{"filter":{"type":"array","value":"[]","raw":"[]","member":false},"attributes":{"type":"array","value":"[\"balance\", \"duration\", \"amount\", \"employment\", \"age\"]","raw":"[\"balance\", \"duration\", \"amount\", \"employment\", \"age\"]","member":false},"sort_by":{"type":"string","value":"id","raw":"\"id\"","member":false},"sort_ascending":{"type":"boolean","value":true,"raw":"true","member":false},"desc":{"type":"boolean","value":false,"raw":"false","member":false},"limit":{"type":"number","value":100,"raw":"100","member":false},"offset":{"type":"number","value":0,"raw":"0","member":false}}` |

## Methods

### updateFilter()

Called when the 'update-filter' event is emitted by the Filter overlay
Inititates a new table request which includes the new filter

**Syntax**

```typescript
updateFilter(newFilter: Object): void
```

**Parameters**

- `newFilter: Object`<br/>
  The new filter

### applyCustomization()

Called when the 'apply' event is emitted by the customize overlay
Inititates a new table request which includes the new attributes

**Syntax**

```typescript
applyCustomization(attributes: Array): void
```

**Parameters**

- `attributes: Array`<br/>
  The attributes to be displayed in the table

### scrollUp()

Scrolls up to page top

**Syntax**

```typescript
scrollUp(): void
```

### sendTableRequest()

Sends the POST /table request and stores the results in the tableRows variable.

**Syntax**

```typescript
sendTableRequest(): void
```

### loadMoreRows()

Dynamically loads more rows from the API when the user scrolls down on the page.

**Syntax**

```typescript
loadMoreRows(): void
```

### applySorting()

Called when the Data Table emits the 'apply-sorting' event.
Sends a table request with the new sorting information

**Syntax**

```typescript
applySorting(sorting: Object): void
```

**Parameters**

- `sorting: Object`<br/>
  The new sorting to be applied.

