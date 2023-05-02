# DataTable

A Data Table component used in the Dataset Explorer
Renders the table based on the props provided

## Props

| Name           | Type     | Description                                                                                                               |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| `table-rows`   | `Array`  | Array with the data for the table rows that should be displayed                                                           |
| `options-data` | `Object` | Object with options data like filters, sorting, etc. Should be equal to the request body used for the POST /table request |

## Events

| Name            | Description                                                     |
| --------------- | --------------------------------------------------------------- |
| `apply-sorting` | <br/>**Arguments**<br/><ul><li>**`sorting: unknown`**</li></ul> |

## Methods

### applySorting()

Triggered when the TableHeader component emits 'apply-sorting'
Emits 'apply-sorting' event to the parent

**Syntax**

```typescript
applySorting(sorting: Object): void
```

**Parameters**

- `sorting: Object`<br/>
  Contains the attribute to sort by and an indicator whether to sort descending
  or ascending

