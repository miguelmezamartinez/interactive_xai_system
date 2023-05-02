# AdminPanel

## Data

| Name                  | Type      | Description                                                                                       | Initial value |
| --------------------- | --------- | ------------------------------------------------------------------------------------------------- | ------------- |
| `experimentList`      | `array`   | Array of all existing experiments                                                                 | `[]`          |
| `showExistingOverlay` | `string`  | Name of an existing experiment for which the overlay is shown. If empty, no overlay is displayed. | `""`          |
| `showNewOverlay`      | `boolean` | Determines if the New Experiment Overlay is shown.                                                | `false`       |

## Methods

### closeOverlay()

Triggered when an overlay emits the 'close' event.
This method closes the overlay.

**Syntax**

```typescript
closeOverlay(): void
```

### sendExperimentRequest()

Sends a request to the api to get the existing experiments

**Syntax**

```typescript
sendExperimentRequest(): void
```

