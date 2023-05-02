# NewExperimentOverlay

An overlay where the user can create a new experiment

## Data

| Name               | Type     | Description                                                                                     | Initial value |
| ------------------ | -------- | ----------------------------------------------------------------------------------------------- | ------------- |
| `name`             | `string` | The experiment name entered by the user                                                         | `""`          |
| `description`      | `string` | The experiment description entered by the user                                                  | `""`          |
| `applications`     | `string` | String of comma-separated loan application ids entered by the user                              | `""`          |
| `applicationArray` | `array`  | Array with the application ids                                                                  | `[]`          |
| `surveyLink`       | `string` | Link to a survey entered by the user                                                            | `""`          |
| `modwhatif`        | `string` | Whether modification and what-if-analysis should be allowed. Can be 'both', 'modonly' or 'none' | `"both"`      |
| `explanation`      | `string` | The explanation type for the experiment. Can be 'lime', 'shap' or 'dice'.                       | `"lime"`      |
| `errorMessages`    | `object` | An object in which errorMessages are saved for every attribute where the input contains errors. | `{}`          |

## Events

| Name    | Description |
| ------- | ----------- |
| `close` | &nbsp;      |

## Methods

### clickCreate()

Triggered when the user clicks 'Create'
Gets a list with existing experiments from the API and calls the validateInput
methods with it.

**Syntax**

```typescript
clickCreate(): void
```

### getBorderStyling()

**Syntax**

```typescript
getBorderStyling(attribute: String): String
```

**Parameters**

- `attribute: String`<br/>
  The attribute/field for which the border styling is applied

**Return value**

Tailwind classes for border styling, red border if there's an error with the
attribute, regular border otherwise

### createExperiment()

Sends a post request to the API to create the experiment.
Emits the 'close' event afterwards.

**Syntax**

```typescript
createExperiment(): void
```

### validateInput()

Validates the inputs and sets error messages if the input is invalid for a
certain attribute/field.
If there are no errors, the createExperiment() method is called.

**Syntax**

```typescript
validateInput(experimentList: Array): void
```

**Parameters**

- `experimentList: Array`<br/>
  List of all existing experiments

