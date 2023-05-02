# DefaultButton

A configurable colored button component

## Slots

| Name      | Description          |
| --------- | -------------------- |
| `default` | The button's content |

## Props

| Name          | Type     | Description                                                                 | Default          |
| ------------- | -------- | --------------------------------------------------------------------------- | ---------------- |
| `color`       | `String` | The button's main color, needs to be a color defined in tailwind.config.cs  | `"primary"`      |
| `hover-color` | `String` | The button's hover color, needs to be a color defined in tailwind.config.cs | `"primary-dark"` |
| `text-color`  | `String` | The button's text color, needs to be a color defined in tailwind.config.cs  | `"white"`        |
| `size`        | `String` | The button's size, can be sm, base, lg, xl, 2xl, ..., 9xl                   | `"lg"`           |

## Methods

### getStyling()

Returns classes for the button's style depending on the props provided

**Syntax**

```typescript
getStyling(): String
```

**Return value**

Tailwind classes for button styling

