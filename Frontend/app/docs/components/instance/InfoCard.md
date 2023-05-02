# InfoCard

This component displays a given instance and the AI recommendation.
Depending on the props it also allows modification and generating the new
explanation and what-if analysis.

## Props

| Name                | Type      | Description                                                                                              |
| ------------------- | --------- | -------------------------------------------------------------------------------------------------------- |
| `instance-info`     | `Object`  | Object with the original instance (attributes as keys and corresponding values)                          |
| `modifiable`        | `Boolean` | Specifies if the user can modify the instance.                                                           |
| `modified-instance` | `Object`  | Object with the user-modified instance (attributes as keys and corresponding values)                     |
| `allow-what-if`     | `Boolean` | Specifies if the 'Generate New Explanation' button is shown and if the user can see the what-if analysis |

## Data

| Name                  | Type      | Description                                                                      | Initial value |
| --------------------- | --------- | -------------------------------------------------------------------------------- | ------------- |
| `dropdownAttribute`   | `string`  | The attribute for which a dropdown menu is displayed, if empty no menu is shown. | `""`          |
| `modificationEnabled` | `boolean` | Specifies whether the user has enabled the modification                          | `false`       |
| `newPrediction`       | `unknown` | The new AI prediction if the instance has been modified                          | `null`        |

## Events

| Name                 | Description                                                                                                 |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| `reset-instance`     |                                                                                                             |
| `apply-modification` | <br/>**Arguments**<br/><ul><li>**`{ attribute: this.dropdownAttribute, value: value }: unknown`**</li></ul> |

## Methods

### sendPredictionRequest()

Sends a request to the API to get the new AI prediction if the instance has been
modified

**Syntax**

```typescript
sendPredictionRequest(): void
```

### resetInstance()

Triggered when user clicks 'Reset'
Resets the InfoCard and emits the 'reset-instance' event

**Syntax**

```typescript
resetInstance(): void
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

Triggered when the dropdown menu emits the 'apply-value' event.
Passes on the information to the parent by emitting the 'apply-modification'
event with the new modification
and calls the sendPredictionRequest() method.

**Syntax**

```typescript
applyValue(value: unknown): void
```

