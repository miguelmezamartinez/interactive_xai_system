# TreeMap

Component for the treemap that visualizes the LIME and SHAP explanations

## Props

| Name          | Type      | Description                                                                                                          |
| ------------- | --------- | -------------------------------------------------------------------------------------------------------------------- |
| `id`          | `String`  | Helps d3 identify this TreeMap. If there are two treemaps displayed at the same time, they should have different ids |
| `exp-type`    | `String`  | The Explanation type. Can be 'lime' or 'shap'                                                                        |
| `instance`    | `Object`  | The instance for which the explanation is shown.                                                                     |
| `whatif`      | `Boolean` | True, if what-if analysis is enabled. Will make the treemap shrink                                                   |
| `detail-view` | `Boolean` | If true the detail view is shown, if false the simple view                                                           |

## Data

| Name            | Type      | Description                                                                                           | Initial value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------- | --------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `windowWidth`   | `object`  | The window's inner width                                                                              | `window.innerWidth`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `href`          | `string`  | The reference provided by the API to check the status of the explanation request and get the results. | `""`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `baseValue`     | `number`  | The base value provided by SHAP                                                                       | `0`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `isLoading`     | `boolean` | Indicates if the treemap is currently loading and controls if the loading animation is shown.         | `true`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `simpleExpData` | `object`  | Explanation data for the simple view                                                                  | `{"name":{"type":"string","value":"Explanation","raw":"\"Explanation\"","member":false},"children":{"type":"array","value":"[ { name: \"positive\", children: [] }, { name: \"negative\", children: [], }, ]","raw":"[ { name: \"positive\", children: [] }, { name: \"negative\", children: [], }, ]","member":false}}`                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `detailExpData` | `object`  | Explanation data for the detail view                                                                  | `{"name":{"type":"string","value":"Explanation","raw":"\"Explanation\"","member":false},"children":{"type":"array","value":"[ { name: \"positive\", children: [ { name: \"financial\", children: [] }, { name: \"personal\", children: [] }, { name: \"loan\", children: [] }, ], }, { name: \"negative\", children: [ { name: \"financial\", children: [] }, { name: \"personal\", children: [] }, { name: \"loan\", children: [] }, ], }, ]","raw":"[ { name: \"positive\", children: [ { name: \"financial\", children: [] }, { name: \"personal\", children: [] }, { name: \"loan\", children: [] }, ], }, { name: \"negative\", children: [ { name: \"financial\", children: [] }, { name: \"personal\", children: [] }, { name: \"loan\", children: [] }, ], }, ]","member":false}}` |

## Methods

### onResize()

Called when the window is resized

**Syntax**

```typescript
onResize(): void
```

### saveData()

Called once the exlanation result has been obtained from the API
The method saves the data in the required structure and calls the
generateTreemap method afterwards

**Syntax**

```typescript
saveData(result: unknown): void
```

**Parameters**

- `result: unknown`<br/>
  The explanation result

### getResult()

As long as the explanation result is null the method sends a request to the API
to check if the result is ready
and then calls itself again with a timeout
If the result is ready, the saveData method is called

**Syntax**

```typescript
getResult(result: unknown, expType: unknown): unknown
```

**Parameters**

- `result: unknown`<br/>
  The explanation result, null if there is no result yet

- `expType: unknown`<br/>
  The current explanation type

### sendExplanationRequest()

Initiates the explanation request to the API
Once the request is accepted by the API it calls the getResult method

**Syntax**

```typescript
sendExplanationRequest(): void
```

### generateTreeMap()

Generates the treemap using d3 based on the explanation data.

**Syntax**

```typescript
generateTreeMap(): void
```

