# Getting Started

A minimal walkthrough to render your first PMD template.

1. Create a template file `greeting.pmd`:

```pmd
Hello, {{name}}!
```

2. Provide a context (JSON) either inline or in a file `greeting.json`:

```json
{"name": "Alice"}
```

3. Render the template with the CLI:

```sh
pmd render greeting.pmd -f greeting.json
```

Rendered result

Using the template and context above the output will be:

```text
Hello, Alice!
```

Alternate options

- Pass context as a JSON string: `-c '{"name": "Bob"}'`
- Render a directory of `.pmd` files: `pmd render templates/ -o output/`
- Inspect template metadata before rendering: `pmd render template.pmd --show-metadata`

Tip: When rendering a single file, PMD will auto-detect a same-name `.json` file (e.g. `greeting.json`) if no context is supplied.
