# ExistingExperimentOverlay

An overlay displaying properties and options regarding an existing experiment

## Props

| Name                         | Type     | Description           |
| ---------------------------- | -------- | --------------------- |
| `experiment-name` *required* | `String` | The experiment's name |

## Data

| Name             | Type     | Description                                    | Initial value |
| ---------------- | -------- | ---------------------------------------------- | ------------- |
| `experimentData` | `object` | The experiment information provided by the API | `{}`          |

## Computed Properties

| Name             | Type      | Description                                                                                                  |
| ---------------- | --------- | ------------------------------------------------------------------------------------------------------------ |
| `experimentLink` | `unknown` | Generates a link to start the experiment based on the experiment name<br/>**Dependencies:** `experimentName` |

## Events

| Name    | Description |
| ------- | ----------- |
| `close` | &nbsp;      |

## Methods

### downloadFile()

Downloads the results file from the API to the user's device

**Syntax**

```typescript
downloadFile(csv: Boolean): void
```

**Parameters**

- `csv: Boolean`<br/>
  true will download results as csv, false as JSON

### resetExperiment()

Resets the experiment after confirmation by the user. This deletes all recorded
answers but not the experiment itself.

**Syntax**

```typescript
resetExperiment(): void
```

### deleteExperiment()

Deletes the entire experiment after confirmation by the user. This includes the
experiment data and all recorded answers.

**Syntax**

```typescript
deleteExperiment(): void
```

### sendExperimentRequest()

Sends a request to the API to get the experiment data and saves it in the
experimentData variable

**Syntax**

```typescript
sendExperimentRequest(): void
```

