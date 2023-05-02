# ExperimentPage

## Data

| Name           | Type      | Description                                                                         | Initial value |
| -------------- | --------- | ----------------------------------------------------------------------------------- | ------------- |
| `started`      | `boolean` | Indicates if the user has started the experiment.                                   | `false`       |
| `expType`      | `unknown` | The explanation type, can be 'lime', 'shap' or 'dice'                               | `String`      |
| `allowMod`     | `boolean` | Indicates if the user is allowed to modify the instance                             | `false`       |
| `allowWhatIf`  | `boolean` | Indicates if the user is allowed to generate what-if analysis                       | `false`       |
| `done`         | `boolean` | Indicates if the user is done with the experiment                                   | `false`       |
| `currentIndex` | `number`  | The current index in the list of instances                                          | `0`           |
| `instanceIds`  | `array`   | Array with all instance ids to be shown to the user                                 | `[]`          |
| `results`      | `array`   | Array with the decision the user has made for each instanc                          | `[]`          |
| `instanceInfo` | `object`  | Object with instance information                                                    | `{}`          |
| `surveyLink`   | `unknown` | Survey the experiment page will link to after the user has finished the experiment. | `null`        |
| `clientId`     | `unknown` | Unique client id for the experiment participant                                     | `Number`      |

## Methods

### goBack()

Jumps back to the previous instance to allow the user to change their decision.

**Syntax**

```typescript
goBack(): void
```

### postResults()

Called when the user has completed the experiment.
Sends the recorded results to the API

**Syntax**

```typescript
postResults(): void
```

### sendExperimentRequest()

Sends an API request to get the experiment information

**Syntax**

```typescript
sendExperimentRequest(): void
```

### submitDecision()

Called when the user clicks 'Approve' or 'Reject'.
Adds the user's decision on the current instance to the results and jumps to the
next instance.

**Syntax**

```typescript
submitDecision(decision: String): void
```

**Parameters**

- `decision: String`<br/>
  Can be 'approve' or 'reject'

### sendInstanceRequest()

Sends an API request to get the instance information.

**Syntax**

```typescript
sendInstanceRequest(): void
```

