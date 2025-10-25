# GTM Labs MCP Workflow Guide

## Purpose
This guide ensures proper version control and changelog tracking for the GTM Labs MCP server.

## When You Update Components

Every time you modify a component in `/homepage/components/`, follow this workflow:

### 1. Make Your Changes
Edit the component file as needed.

### 2. Commit with Conventional Commits
```bash
# For new features or changes
git add components/ui/[component-name].tsx
git commit -m "feat: [component-name] - [brief description]"

# For bug fixes
git commit -m "fix: [component-name] - [brief description]"

# For styling updates
git commit -m "style: [component-name] - [brief description]"

# For code refactoring
git commit -m "refactor: [component-name] - [brief description]"

# Examples:
# git commit -m "feat: hero-section - add gradient animation"
# git commit -m "fix: two-column-layout - fix mobile spacing"
# git commit -m "style: how-we-help-section - update border radius"
```

### 3. Create Release Tags (for stable versions)
When you have a stable set of changes ready for release:

```bash
# Tag the release
git tag -a v1.0.0 -m "Release v1.0.0: Initial stable release"
git tag -a v1.1.0 -m "Release v1.1.0: Updated hero animations"
git tag -a v1.2.0 -m "Release v1.2.0: New two-column layouts"

# Push tags to remote
git push origin v1.0.0
git push origin --tags  # or push all tags at once
```

### 4. MCP Auto-Indexing
The MCP server will automatically:
- Track all commits as snapshots
- Index all tagged releases
- Generate changelogs per component
- Allow users to query specific versions

## Version Querying Examples

Users can request components via MCP like:

```
"Get hero-section"                    → Returns latest version
"Get hero-section v1.1.0"            → Returns tagged version
"Get hero-section at commit abc123"   → Returns specific commit
"Show changelog for hero-section"     → Shows all version history
```

## Security Notes

The MCP automatically:
- Excludes `.env*`, `*secrets*`, `*private*` files
- Redacts API keys and credentials
- Removes mentions of: MyMarky, UseQueue, and other proprietary tools
- Only exposes public-facing code (components, utils, configs)

## Component Categories in MCP

```
gtm-labs://
├── components/sections/     (hero, two-column, features, etc.)
├── components/navigation/   (navbar, footer, etc.)
├── components/animations/   (all animation components)
├── components/ui/           (buttons, cards, etc.)
├── layouts/                 (page layouts and templates)
├── config/                  (tailwind, design tokens, etc.)
├── utils/                   (helper functions, utilities)
└── scaffolds/               (full project templates)
```

## Tips

- **Commit often**: Every meaningful change creates a snapshot
- **Tag strategically**: Only tag when you have a stable, tested version
- **Descriptive messages**: Help future you understand what changed
- **Test before tagging**: Make sure everything works before creating a release tag

---

*This workflow ensures your GTM Labs website code is versioned, tracked, and reusable via MCP for future projects.*
