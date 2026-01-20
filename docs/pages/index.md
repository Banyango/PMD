# PMD

PMD is a lightweight templating tool for building prompt and markdown templates with metadata, context, and simple control flow.

Key features

- Simple variable substitution with JSON contexts
- Template metadata for task information (e.g. `@task`, `@owner`)
- Conditionals and loops for dynamic sections
- Include files to compose templates across multiple fragments
- CLI for rendering and metadata inspection (`pmd render`, `pmd metadata`)

Quick example

Create `hello.pmd` containing:

```pmd
Hello, {{name}}!
```

Render with a JSON context:

```sh
pmd render hello.pmd -c '{"name": "World"}'
```

Rendered result

Given the template above and the context `{"name": "World"}`, the rendered output will be:

```text
Hello, World!
```

See also: `Getting Started`, `Language Reference` pages (Contexts, Metadata, Conditionals, Loops, Include Files).
