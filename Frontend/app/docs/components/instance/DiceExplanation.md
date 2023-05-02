# DiceExplanation

A component for displaying the DiCE explanation.
It shows 5 different tables with the original instance and one counterfactual
each time.
The user can navigate through these tables with arrow buttons.

## Props

| Name                       | Type     | Description                                                     |
| -------------------------- | -------- | --------------------------------------------------------------- |
| `instance-info` *required* | `Object` | The instance (loan application) to be used for the explanation. |

## Data

| Name              | Type      | Description                                                                                     | Initial value                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ----------------- | --------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `counterfactuals` | `array`   | An array of all counterfactual instances                                                        | `[]`                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `index`           | `number`  | The current index when moving through the counterfactual array                                  | `0`                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `description`     | `string`  | Description for DiCE that shows when the user hovers over the info button                       | `"The goal of counterfactual explanations is to modify the values of a given loan application in such a way that the AI prediction of the modified instance leads to the opposite prediction. In the table below, you can switch between 5 counterfactuals for the loan application above. The second row shows the modified values that lead to the new prediction while the first row shows the original values for these attributes."` |
| `hover`           | `boolean` | True while the user hovers over the info button. In that case the description overlay is shown. | `false`                                                                                                                                                                                                                                                                                                                                                                                                                                   |

## Methods

### handleClick()

Handles clicks on the arrow buttons to move through the counterfactuals

**Syntax**

```typescript
handleClick(direction: String): void
```

**Parameters**

- `direction: String`<br/>
  The direction of the arrow, can be 'left' or 'right'

### getArrowStyling()

Returns classes for the arrow's style depending on the current position in the
counterfactuals.
Makes the button grayed out, when it's not possible to move left/right further

**Syntax**

```typescript
getArrowStyling(direction: String): String
```

**Parameters**

- `direction: String`<br/>
  The direction of the arrow, can be 'left' or 'right'

**Return value**

Tailwind classes for arrow styling

### sendDiceRequest()

Sends a request to the API to get the counterfactuals and saves them to the
counterfactuals variable

**Syntax**

```typescript
sendDiceRequest(): void
```

### getBaseRow()

Sends a request to the API to get the counterfactuals and saves them to the
counterfactuals variable

**Syntax**

```typescript
getBaseRow(cfRow: unknown): unknown
```

