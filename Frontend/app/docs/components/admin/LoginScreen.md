# LoginScreen

A login screen component that controls access to the admin panel

## Data

| Name        | Type     | Description                                         | Initial value |
| ----------- | -------- | --------------------------------------------------- | ------------- |
| `userInput` | `string` | The password typed into the input field by the user | `""`          |

## Methods

### clickLogin()

Is trigerred when the user clicks the login button.
Sends the password to the API to check if it's correct.
Shows an error message if the password is wrong or emits the 'logged-in' event
if it's correct.

**Syntax**

```typescript
clickLogin(): void
```

