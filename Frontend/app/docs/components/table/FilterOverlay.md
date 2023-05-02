# FilterOverlay

Component for the overlay in which the user can add filters.

## Props

| Name              | Type    | Description                                            |
| ----------------- | ------- | ------------------------------------------------------ |
| `current-filters` | `Array` | Array with information about currently applied filters |

## Data

| Name              | Type     | Description                                                                          | Initial value         |
| ----------------- | -------- | ------------------------------------------------------------------------------------ | --------------------- |
| `newFilters`      | `object` | New filters to be applied                                                            | `this.currentFilters` |
| `filterAttribute` | `string` | The attribute for which the filter menu is shown, when empty no filter menu is shown | `""`                  |

## Events

| Name            | Description                                                       |
| --------------- | ----------------------------------------------------------------- |
| `update-filter` | <br/>**Arguments**<br/><ul><li>**`newFilters: object`**</li></ul> |

## Methods

### removeAllFilters()

Triggered when the user clicks 'Reset All'. Emits the update-filter event with
an empty array of new filters.

**Syntax**

```typescript
removeAllFilters(): void
```

### addFilter()

Adds a new filter. Emits the update-filter event with an array containing the
new filter in addition to existing ones.

**Syntax**

```typescript
addFilter(filter: unknown): void
```

**Parameters**

- `filter: unknown`<br/>
  Object representing the new filter

### removeFilter()

Removes a filter.

**Syntax**

```typescript
removeFilter(attribute: unknown): void
```

**Parameters**

- `attribute: unknown`<br/>
  The attribute for which the filter should be removed

### findFilter()

Finds existing filter for a given attribute

**Syntax**

```typescript
findFilter(attribute: unknown): Object
```

**Return value**

Existing filter for the attribute, null if there is none

