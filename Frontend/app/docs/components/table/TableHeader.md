# TableHeader

A component for a table header

## Props

| Name           | Type      | Description                                             |
| -------------- | --------- | ------------------------------------------------------- |
| `labels`       | `Object`  | Object with labels for the attributes                   |
| `descriptions` | `Object`  | Object with descriptions for the attributes             |
| `attributes`   | `Array`   | Array with all attributes to be displayed in the header |
| `sort_by`      | `String`  | Attribute by which the data is sorted                   |
| `desc`         | `Boolean` | true if data is sorted descending, false otherwise      |

## Data

| Name        | Type     | Description                                                                                    | Initial value |
| ----------- | -------- | ---------------------------------------------------------------------------------------------- | ------------- |
| `hoverText` | `string` | The text that should be displayed when the user hovers over the info icon next to an attribute | `""`          |

## Events

| Name            | Description                                                                                                                                                                 |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `apply-sorting` | <br/>**Arguments**<br/><ul><li>**`{         sort_by: attribute,         desc: this.desc == false && this.sort_by == attribute ? true : false,       }: unknown`**</li></ul> |

## Methods

### applySorting()

Triggered when an attribute is clicked in the table header.
Emits 'apply-sorting' event to the parent to sort by that attribute.

**Syntax**

```typescript
applySorting(attribute: String): void
```

**Parameters**

- `attribute: String`<br/>
  The attribute clicked

