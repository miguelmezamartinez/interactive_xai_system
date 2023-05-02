# CustomizeOverlay

Component for the overlay in which the user can customize the attributes
displayed in the table.

## Props

| Name                 | Type    | Description |
| -------------------- | ------- | ----------- |
| `current-attributes` | `Array` | &nbsp;      |

## Data

| Name                 | Type    | Description | Initial value                 |
| -------------------- | ------- | ----------- | ----------------------------- |
| `selectedAttributes` | `array` |             | `[...this.currentAttributes]` |

## Events

| Name    | Description                                                              |
| ------- | ------------------------------------------------------------------------ |
| `apply` | <br/>**Arguments**<br/><ul><li>**`selectedAttributes: array`**</li></ul> |

## Methods

### addAttribute()

**Syntax**

```typescript
addAttribute(attr: unknown): void
```

### applyChanges()

**Syntax**

```typescript
applyChanges(): void
```

