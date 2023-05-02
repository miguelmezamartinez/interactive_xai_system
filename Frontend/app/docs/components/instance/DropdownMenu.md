# DropdownMenu

Component for the dropdown menu used to modify attribute values

## Props

| Name             | Type     | Description                                         |
| ---------------- | -------- | --------------------------------------------------- |
| `original-value` | `String` | The value of the attribute in the original instance |
| `selected-value` | `String` | The current value of the attribute                  |
| `attribute`      | `String` | The attribute name                                  |

## Data

| Name          | Type     | Description                                                    | Initial value        |
| ------------- | -------- | -------------------------------------------------------------- | -------------------- |
| `sliderValue` | `object` | The value the slider is currently at for continuous attributes | `this.selectedValue` |

## Events

| Name          | Description                                                          |
| ------------- | -------------------------------------------------------------------- |
| `apply-value` | <br/>**Arguments**<br/><ul><li>**`originalValue: string`**</li></ul> |

## Methods

### cancel()

Called when the user clicks cancel.
Emits the 'apply-value' event with the original value

**Syntax**

```typescript
cancel(): void
```

### getValueStyling()

Returns classes for the value styling depending on if it's modified

**Syntax**

```typescript
getValueStyling(attribute: String): String
```

**Parameters**

- `attribute: String`<br/>
  The attribute name

**Return value**

Tailwind classes for attribute value styling

### applyValue()

Called when the user clicks apply.
Applies the newly selected value.

**Syntax**

```typescript
applyValue(value: unknown): void
```

