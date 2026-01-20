# Include Files

Reuse template fragments using `{% include "file.pmd" %}`. Includes are resolved relative to the including template's directory.

Example

`header.pmd`:

```pmd
This is the header content.
```

`page.pmd`:

```pmd
{% include "header.pmd" %}

# Page Title

Content goes here using the same context.
```

Rendered result

When rendering `page.pmd`, the output will include the header content followed by the page body:

```text
This is the header content.

# Page Title

Content goes here using the same context.
```

Behavior

- Included files have access to the same rendering context as the parent template.
- Paths are resolved relative to the parent template's directory (the CLI and renderer set `base_path`).
- Avoid circular includes; they can cause infinite loops or errors.

Tip: Use includes for headers, footers, and small shared components to keep templates DRY and maintainable.
