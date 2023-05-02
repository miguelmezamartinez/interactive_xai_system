# FilterMenu

Component for the filter menu for a certain attribute.

## Props

| Name             | Type     | Description                                                                                                  |
| ---------------- | -------- | ------------------------------------------------------------------------------------------------------------ |
| `current-filter` | `Object` | Object representing the currently applied filter for this attribute. Should be empty if there are no filters |
| `attribute`      | `String` | The attribute for which the filter menu should be displayed                                                  |

## Data

| Name             | Type      | Description                                                                                     | Initial value |
| ---------------- | --------- | ----------------------------------------------------------------------------------------------- | ------------- |
| `allowedRange`   | `unknown` | The allowed range for a continuous attribute, can be modified by user through moving the slider | `Array`       |
| `selectedValues` | `unknown` | The attribute values that should be filtered by (for categorical attributes)                    | `Array`       |

## Events

| Name     | Description                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------ |
| `cancel` |                                                                                                                    |
| `apply`  | <br/>**Arguments**<br/><ul><li>**`{ attribute: this.attribute, values: this.selectedValues, }: object`**</li></ul> |

## Methods

### cancel()

Triggered when the user clicks 'Cancel'
Emits the 'cancel' event

**Syntax**

```typescript
cancel(): void
```

### applyChanges()

Triggered when the user clicks 'Apply'
Emits the 'apply' event and sends the new filter object as payload

**Syntax**

```typescript
applyChanges(): void
```

