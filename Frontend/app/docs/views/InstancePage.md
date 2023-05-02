# InstancePage

Component for the instance/application page. Contains navigation buttons and the
instance view.

## Data

| Name           | Type     | Description                                                                                 | Initial value           |
| -------------- | -------- | ------------------------------------------------------------------------------------------- | ----------------------- |
| `id`           | `object` | The instance id. Provided by an url parameter                                               | `this.$route.params.id` |
| `instanceInfo` | `object` | The instance information.                                                                   | `{}`                    |
| `expType`      | `string` | The explanation type to be shown, can be 'lime', 'lime_orig', 'shap', 'shap_orig' or 'dice' | `"dice"`                |

## Methods

### switchExp()

Triggered when the user switches the explanation type

**Syntax**

```typescript
switchExp(expType: String): void
```

**Parameters**

- `expType: String`<br/>
  The new explanation type, can be 'lime', 'lime_orig', 'shap', 'shap_orig' or 'dice'

### backToDataset()

Navigates back to the dataset explorer.

**Syntax**

```typescript
backToDataset(): void
```

### sendInstanceRequest()

Sends an API request to get the instance information.

**Syntax**

```typescript
sendInstanceRequest(): void
```
